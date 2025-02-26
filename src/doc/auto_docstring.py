"""'''
A module to update top-level docstrings in Python files based on detected changes.

This module provides the `DocstringUpdater` class, which automates the process of 
analyzing Python files for changes, generating new docstrings using a language 
model, and updating the files with the new docstrings.

Key Classes:
- `DocstringUpdater`: Detects changes in Python files, generates new top-level 
  docstrings using an LLM (Language Model), and updates the files in place.

Notable Dependencies:
- `os`: Used for directory and file operations.
- `re`: Utilized for regex operations to identify existing docstrings.
- `json`: Employed for reading and writing hash data to track file changes.
- `hashlib`: Used to compute hashes of file contents for change detection.
- `LLM` from `src.utils.openai_utils`: A language model used to generate docstrings.
- `cfg` from `src.config`: Configuration settings, such as directories to exclude.

Overall Purpose and Functionality:
The main purpose of this module is to ensure the docstrings in Python files are
up-to-date with the latest changes in the code. It does so by computing a hash 
of the code (excluding existing docstrings), comparing it against stored hashes 
to detect changes, and then using an LLM to generate and insert updated docstrings 
where necessary. The `DocstringUpdater` class also provides functionality to 
recursively update docstrings in all Python files within a specified directory.
'''"""

import os
import re
import json
import hashlib

from src.config import cfg
from src.utils.openai_utils import LLM


class DocstringUpdater:
    """
    A class to detect changes in Python files, generate docstrings for them
    if they’ve changed, and replace their top-level docstring in place.
    """

    DOCSTRING_REGEX = re.compile(
        r'^"""(.*?)"""',
        flags=re.DOTALL
    )
    HASH_DB_FILENAME = "cache/.docstring_cache.json"

    def __init__(self):
        """
        :param llm: An instance of the LLM class to generate docstrings.
        """
        if not os.path.exists("cache"):
            os.mkdir("cache")
        self.llm = LLM(system_message="You are an expert Python docstring generator.")
        self.hash_db = self._load_hash_db()

    def _load_hash_db(self) -> dict:
        """
        Loads a JSON file that stores file hashes to track code changes.

        :return: A dictionary with file paths as keys and their cached hashes as values.
        """
        if os.path.exists(self.HASH_DB_FILENAME):
            with open(self.HASH_DB_FILENAME, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_hash_db(self):
        """
        Saves the in-memory hash dictionary to a JSON file.
        """
        with open(self.HASH_DB_FILENAME, "w", encoding="utf-8") as f:
            json.dump(self.hash_db, f, indent=2)

    def _compute_file_hash(self, file_content: str) -> str:
        """
        Computes a hash for the file content to detect changes.

        :param file_content: The entire text content of the file.
        :return: A hex digest string for the hash.
        """
        return hashlib.sha256(file_content.encode("utf-8")).hexdigest()

    def _extract_code_without_top_level_docstring(self, content: str) -> str:
        """
        Removes the top-level docstring from the file content, if present.

        :param content: Full content of a .py file.
        :return: The content with the top-level docstring (if any) removed.
        """
        # Attempt to match only if the docstring starts at the very beginning of the file.
        match = self.DOCSTRING_REGEX.match(content)
        if match:
            # docstring_text = match.group(1)  # If you need the old docstring for any reason
            # Strip out everything from the opening triple quotes to the closing triple quotes.
            content_without_docstring = content[match.end():].lstrip("\n")
            return content_without_docstring
        return content

    def _insert_top_level_docstring(self, docstring: str, content: str) -> str:
        """
        Inserts a triple-quoted docstring at the top of the file, preserving PEP257 style.

        :param docstring: The docstring content to insert (without triple quotes).
        :param content: The rest of the file content (with no existing top-level docstring).
        :return: File content with the new top-level docstring at the beginning.
        """
        # Typically, a top-level docstring is placed at the start of the file.
        # You may want to insert it after shebangs, encoding lines, or imports.
        # For simplicity, this example puts it right at the start.

        formatted_docstring = f'"""{docstring}"""\n\n{content}'
        return formatted_docstring

    def _generate_docstring_for_file(self, code: str) -> str:
        """
        Uses the LLM to generate a docstring for the entire code file.

        :param code: The code of the file (with the old docstring removed).
        :return: The newly generated docstring (no triple quotes).
        """
        prompt = (
            "Analyze the following Python code and produce a top-level docstring "
            "that follows PEP257 and Python best practices.  The docstring should:"
            " - Key classes/functions and their roles\n"
            " - Notable dependencies/imports\n"
            " - Overall purpose and functionality\n\n"
            f"{code}\n\n"
            "Docstring only (do not enclose in triple quotes)."
        )
        # Request the docstring from the LLM
        new_docstring = self.llm.prompt(prompt)
        # Ensure it doesn’t inadvertently include triple quotes
        new_docstring = new_docstring.replace('"""', "'''")
        return new_docstring.strip()

    def update_docstring_in_file(self, file_path: str):
        """
        Checks if the code has changed; if so, generates a new top-level docstring
        and updates the file in place. Otherwise, skips.

        :param file_path: Path to the .py file to be updated.
        """
        # Read current file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Strip out the existing docstring
        content_no_docstring = self._extract_code_without_top_level_docstring(content)

        # Compute and compare hash of code-only content
        current_code_hash = self._compute_file_hash(content_no_docstring)
        stored_hash = self.hash_db.get(file_path)

        if len(content_no_docstring.strip()) == 0:
            print(f"No code found in {file_path}, skipping...")
            return

        if stored_hash == current_code_hash:
            print(f"No code changes detected for {file_path}, skipping.")
            return

        # Generate a new docstring using the LLM
        new_docstring = self._generate_docstring_for_file(content_no_docstring)

        # Insert the new docstring on top
        updated_content = self._insert_top_level_docstring(new_docstring, content_no_docstring)

        # Write updated file with new docstring
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        # Now strip out the new docstring again and compute hash for the updated code
        new_code_hash = self._compute_file_hash(
            self._extract_code_without_top_level_docstring(updated_content)
        )
        self.hash_db[file_path] = new_code_hash
        self._save_hash_db()

        print(f"Updated docstring for {file_path}.")


    def update_docstrings_in_directory(self, directory: str):
        """
        Recursively walks through a directory, updating docstrings for all .py files.

        :param directory: Path to the directory to traverse.
        """
        print("Updating codebase docstrings...")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in cfg.exclude_dirs]
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    self.update_docstring_in_file(file_path)
        print("Done updating codebase docstrings...")


# Example usage:
# if __name__ == "__main__":
#     updater = DocstringUpdater()
#     updater.update_docstrings_in_directory("path/to/your/python/codebase")
