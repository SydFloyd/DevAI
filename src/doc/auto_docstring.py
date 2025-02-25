import os
import re
import json
import hashlib

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
    HASH_DB_FILENAME = ".docstring_hashes.json"

    def __init__(self):
        """
        :param llm: An instance of the LLM class to generate docstrings.
        """
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
            "that follows PEP257 and Python best practices:\n\n"
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
        Checks if the file has changed; if so, generates a new top-level docstring
        and updates the file in place. Otherwise, skips.

        :param file_path: Path to the .py file to be updated.
        """
        # Read current file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Compute current hash
        current_hash = self._compute_file_hash(content)
        stored_hash = self.hash_db.get(file_path)

        # If hashes match, skip processing
        if stored_hash == current_hash:
            print(f"No changes detected for {file_path}, skipping.")
            return

        # Remove old top-level docstring
        content_no_docstring = self._extract_code_without_top_level_docstring(content)

        # Generate a new docstring using the LLM
        new_docstring = self._generate_docstring_for_file(content_no_docstring)

        # Insert the new docstring
        updated_content = self._insert_top_level_docstring(new_docstring, content_no_docstring)

        # Write updated file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

        # Update the file’s hash in the DB
        new_hash = self._compute_file_hash(updated_content)
        self.hash_db[file_path] = new_hash
        self._save_hash_db()

        print(f"Updated docstring for {file_path}.")

    def update_docstrings_in_directory(self, directory: str):
        """
        Recursively walks through a directory, updating docstrings for all .py files.

        :param directory: Path to the directory to traverse.
        """
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".py"):
                    file_path = os.path.join(root, file_name)
                    self.update_docstring_in_file(file_path)


# Example usage:
# if __name__ == "__main__":
#     llm = LLM(system_message="You are an expert Python docstring generator.")
#     updater = DocstringUpdater(llm)
#     updater.update_docstrings_in_directory("path/to/your/python/codebase")
