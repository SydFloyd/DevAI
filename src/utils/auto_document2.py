import os
import ast
import hashlib
import json
from collections import defaultdict
import tiktoken

from src.config import cfg
from src.utils.openai_utils import get_client, chat

class LLM:
    def __init__(self, system_message, temperature=0.7):
        self.system_message = system_message
        self.temperature = temperature
        self.client = get_client()
    def prompt(self, prompt):
        chat(self.client, prompt, system_message=self.system_message, temperature=self.temperature)

if not os.path.exists("cache"):
    os.mkdir("cache")
CACHE_FILE = "cache/summary_cache.json"
IGNORED_DIRS = cfg.exclude_dirs

CHUNK_SIZE = 32_000 # tokens

def load_cache(cache_file=CACHE_FILE):
    """Load summaries for files and directories from a local JSON cache."""
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"files": {}, "directories": {}, "codebase": {}}

def save_cache(cache, cache_file=CACHE_FILE):
    """Save updated cache to disk as JSON."""
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 hash of a file's contents."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

def combine_hashes(hashes):
    """Combine multiple hashes into one by hashing the concatenation of them."""
    combined = hashlib.sha256("".join(hashes).encode("utf-8")).hexdigest()
    return combined

def count_tokens(text: str) -> int:
    """Approximate token count for a given text."""
    enc = tiktoken.get_encoding("cl100k_base")  # or appropriate encoder
    return len(enc.encode(text))

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE):
    """Split text into chunks of up to `chunk_size` tokens."""
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    for i in range(0, len(tokens), chunk_size):
        yield enc.decode(tokens[i:i+chunk_size])

def ast_parse_file(filepath: str):
    """
    Parse a Python file using AST to extract structured info.
    Returns a dict with classes, functions, imports, docstring, etc.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"error": f"Could not parse {filepath}", "source": source}

    classes = []
    functions = []
    imports = []
    docstring = ast.get_docstring(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                imports.append(f"{mod}.{alias.name}")

    return {
        "filepath": filepath,
        "docstring": docstring,
        "classes": classes,
        "functions": functions,
        "imports": list(set(imports)),
        "source": source
    }

def summarize_large_text(llm, text: str, chunk_label: str = "file/directory"):
    """
    Summarize large text by chunking if necessary.
    Return a cohesive summary of the entire text.
    """
    if count_tokens(text) <= CHUNK_SIZE:
        # Summarize in one go
        return llm.prompt(f"Summarize the following {chunk_label} contents:\n{text}")
    else:
        # Summarize chunk by chunk
        partial_summaries = []
        for idx, chunk in enumerate(chunk_text(text, CHUNK_SIZE)):
            chunk_summary = llm.prompt(
                f"You are summarizing chunk #{idx} of a large {chunk_label}.\n"
                "Focus on key functionalities, classes, dependencies, purpose, etc.\n"
                f"{chunk}"
            )
            partial_summaries.append(chunk_summary)

        # Combine partial summaries
        combined_summary = llm.prompt(
            "Combine the following chunk-level summaries into one cohesive final summary:\n\n"
            + "\n\n".join(partial_summaries)
        )
        return combined_summary

def summarize_file_ast(llm, file_info: dict):
    """
    Summarize a file using AST data (reducing token usage).
    Fall back to full-text summarization if there's an error or you want more detail.
    """
    prompt = (
        "You are generating documentation for this Python file.\n"
        "Summarize key classes, functions, imports, and the file's overall purpose.\n"
        f"File: {file_info['filepath']}\n"
        f"Docstring: {file_info.get('docstring','No top-level docstring.')}\n"
        f"Classes: {file_info.get('classes',[])}\n"
        f"Functions: {file_info.get('functions',[])}\n"
        f"Imports: {file_info.get('imports',[])}\n"
    )
    return llm.prompt(prompt)

def get_file_summary(llm, filepath: str, cache: dict, use_ast=True) -> str:
    """
    Return a cached or newly generated summary for a single file.
    """
    file_hash = compute_sha256(filepath)
    cached_entry = cache["files"].get(filepath)

    # Check if we can reuse the cached summary
    if cached_entry and cached_entry["hash"] == file_hash:
        return cached_entry["summary"]

    # Otherwise, re-summarize
    if use_ast:
        file_info = ast_parse_file(filepath)
        if "error" in file_info or not file_info.get("source"):
            # Fallback to full text summarization
            with open(filepath, "r", encoding="utf-8") as f:
                file_content = f.read()
            summary = summarize_large_text(llm, file_content, chunk_label="file")
        else:
            # Summarize with AST-based approach
            summary = summarize_file_ast(llm, file_info)
    else:
        # Summarize entire file text
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
        summary = summarize_large_text(llm, file_content, chunk_label="file")

    # Update cache
    cache["files"][filepath] = {
        "hash": file_hash,
        "summary": summary
    }
    return summary

def summarize_directory(
    llm,
    dir_path: str,
    file_summaries: dict,
    cache: dict,
    embed_raw_code_in_dir_summary: bool = True
) -> str:
    """
    Summarize a directory. Optionally include the raw code for all files if your context window is huge.
    Otherwise, rely on file-level summaries.

    `file_summaries` is a dict of {filepath: summary_text}.
    """
    # Compute the combined directory hash from all file hashes
    file_hashes = []
    for fp in file_summaries.keys():
        file_hashes.append(cache["files"][fp]["hash"])
    dir_hash = combine_hashes(sorted(file_hashes))

    # Check cached directory summary
    cached_entry = cache["directories"].get(dir_path)
    if cached_entry and cached_entry["dir_hash"] == dir_hash:
        return cached_entry["summary"]

    # No valid cache; create a new directory-level summary
    # Optionally embed raw code if we have huge context capacity
    if embed_raw_code_in_dir_summary:
        # Concatenate all file contents for a single directory-level summary
        dir_text_chunks = []
        for fp in file_summaries.keys():
            with open(fp, "r", encoding="utf-8") as f:
                dir_text_chunks.append(f"### {fp}\n{f.read()}")
        full_dir_text = "\n\n".join(dir_text_chunks)

        # Summarize the entire directory's raw code
        directory_summary = summarize_large_text(llm, full_dir_text, chunk_label="directory")
    else:
        # Summarize by referencing file-level summaries only
        prompt_pieces = []
        for fp, fsum in file_summaries.items():
            prompt_pieces.append(f"FILE: {fp}\nSUMMARY:\n{fsum}\n")
        combined_summaries = "\n".join(prompt_pieces)

        directory_summary = summarize_large_text(llm, combined_summaries, chunk_label="directory summaries")

    # Store directory summary in cache
    cache["directories"][dir_path] = {
        "dir_hash": dir_hash,
        "summary": directory_summary
    }
    return directory_summary

def build_documentation(
    root_dir: str,
    use_ast: bool = True,
    embed_raw_code_in_dir_summary: bool = False
) -> str:
    """
    Main pipeline to:
      1. Summarize each file (with caching).
      2. Summarize each directory from file-level summaries (with caching).
      3. Summarize the entire codebase from directory-level summaries (with caching).
    """
    llm = LLM(system_message="You are an expert in generating complete and concise documentation of code.")
    cache = load_cache()

    # Gather Python files
    dir_to_files = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        py_files = [os.path.join(dirpath, f) for f in filenames if f.endswith(".py")]
        if py_files:
            dir_to_files[dirpath].extend(py_files)

    # 1) Summarize each file
    directory_summaries = {}
    for dir_path, files in dir_to_files.items():
        file_sums = {}
        for fpath in files:
            file_sums[fpath] = get_file_summary(llm, fpath, cache, use_ast=use_ast)

        # 2) Summarize directory based on file-level data
        directory_summary = summarize_directory(
            llm,
            dir_path,
            file_sums,
            cache,
            embed_raw_code_in_dir_summary=embed_raw_code_in_dir_summary
        )
        directory_summaries[dir_path] = directory_summary

    # 3) Summarize entire codebase
    # Build a combined hash of all directory hashes
    dir_hashes = []
    for dpath, dsummary in directory_summaries.items():
        dir_hashes.append(cache["directories"][dpath]["dir_hash"])
    codebase_hash = combine_hashes(sorted(dir_hashes))

    cached_codebase = cache["codebase"].get("hash")
    if cached_codebase and cached_codebase == codebase_hash:
        # If codebase hasn't changed, reuse final summary
        final_summary = cache["codebase"]["summary"]
    else:
        # Re-generate top-level summary
        # If your context window is truly massive (e.g. 128k), you can embed all directory summaries
        # directly. Otherwise, chunk them if they exceed the limit.
        all_dir_summaries_text = []
        for dpath, dsummary in directory_summaries.items():
            all_dir_summaries_text.append(f"DIR: {dpath}\nSUMMARY:\n{dsummary}\n")
        combined_text = "\n".join(all_dir_summaries_text)

        final_summary = summarize_large_text(llm, combined_text, chunk_label="codebase")

        # Cache the codebase summary
        cache["codebase"]["hash"] = codebase_hash
        cache["codebase"]["summary"] = final_summary

    # Write out the updated cache
    save_cache(cache)

    return final_summary

# Example usage:
# doc = build_documentation(
#     "/path/to/repo",
#     use_ast=True,
#     embed_raw_code_in_dir_summary=True  # If you want to feed entire directory contents for GPT-4 128k
# )
# print(doc)
