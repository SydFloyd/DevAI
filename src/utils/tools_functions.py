from pathlib import Path
import os

def build_directory_tree(start_path=".", exclude_dirs=None):
    """
    Recursively builds an ASCII representation of the directory structure 
    starting from `start_path`, returns it as a string.

    :param start_path: Path to the root directory. Defaults to current directory.
    :param exclude_dirs: List of directory names to exclude (e.g. ['.venv']).
                        By default, excludes ['.venv'].
    :return: A string representing the directory tree.
    """
    print("build_directory_tree function called.")
    if exclude_dirs is None:
        exclude_dirs = [".venv", ".git", "__pycache__", "key.txt"]  # Default to excluding .venv

    lines = []

    # Print the root directory name at the top
    lines.append(start_path.rstrip("/"))

    def _build_tree(current_path, prefix=""):
        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            # If permission denied, indicate and return
            lines.append(prefix + "└── [Permission Denied]")
            return
        
        # Filter out any directories that should be excluded
        filtered_entries = []
        for entry in entries:
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path) and entry in exclude_dirs:
                # Skip excluded directories
                continue
            filtered_entries.append(entry)
        
        for index, entry in enumerate(filtered_entries):
            full_path = os.path.join(current_path, entry)
            
            # Check if this is the last item in the directory to adjust symbols
            is_last_item = (index == len(filtered_entries) - 1)
            branch_symbol = "└── " if is_last_item else "├── "
            extension_prefix = "    " if is_last_item else "│   "

            lines.append(prefix + branch_symbol + entry)

            # If it's a directory, recurse
            if os.path.isdir(full_path):
                _build_tree(full_path, prefix + extension_prefix)

    _build_tree(start_path)
    return "\n".join(lines)


def read_file(file_path: str, project_root: str = ".") -> str:
    """
    Reads and returns the content of a file in a given project root.
    
    :param file_path: Path to the file to be read (can be relative to project_root).
    :param project_root: The root directory within which the file must exist.
    :return: String content of the file.
    :raises ValueError: If the resolved file path is outside the project_root.
    :raises FileNotFoundError: If the file does not exist.
    :raises IsADirectoryError: If the path points to a directory instead of a file.
    """
    print("read_file function called.")
    # Resolve the full, absolute path of both project_root and the target file.
    root_path = Path(project_root).resolve()
    target_path = (root_path / file_path).resolve()

    # Check that target_path is within the project_root (basic sandboxing).
    if not str(target_path).startswith(str(root_path)):
        raise ValueError(f"Attempted to access file outside of project root: {target_path}")

    # Ensure the target is a file and exists.
    if not target_path.exists():
        raise FileNotFoundError(f"No such file or directory: {target_path}")
    if target_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {target_path}")

    # Read and return the file’s contents.
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(file_path: str, new_content: str, project_root: str = ".") -> None:
    """
    Overwrites (or creates) a file in the given project root with new_content.
    
    :param file_path: Path to the file to be written (can be relative to project_root).
    :param new_content: The string content to write to the file.
    :param project_root: The root directory within which the file must be written.
    :raises ValueError: If the resolved file path is outside the project_root.
    :raises IsADirectoryError: If the path is a directory.
    """
    print("write_file function called.")
    # Resolve the full, absolute path of both project_root and the target file.
    root_path = Path(project_root).resolve()
    target_path = (root_path / file_path).resolve()

    # Check that target_path is within the project_root (basic sandboxing).
    if not str(target_path).startswith(str(root_path)):
        raise ValueError(f"Attempted to write file outside of project root: {target_path}")

    # If the target path is an existing directory, raise an error.
    if target_path.exists() and target_path.is_dir():
        raise IsADirectoryError(f"Cannot write to a directory: {target_path}")

    # Make sure the parent directory exists; create it if necessary.
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Write (overwrite) the file with new_content.
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_content)
