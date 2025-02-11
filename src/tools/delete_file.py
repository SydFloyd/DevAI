from pathlib import Path

def delete_file(file_path: str, project_root: str = ".") -> None:
    """
    Deletes a file from the given project root.
    
    :param file_path: Path to the file to be deleted (can be relative to project_root).
    :param project_root: The root directory within which the file must exist.
    :raises ValueError: If the resolved file path is outside the project_root.
    :raises FileNotFoundError: If the file does not exist.
    :raises IsADirectoryError: If the path points to a directory instead of a file.
    """
    print(f"delete_file function called on {file_path}.")
    root_path = Path(project_root).resolve()
    target_path = (root_path / file_path).resolve()

    # Check if the target path is within the project root
    if not str(target_path).startswith(str(root_path)):
        raise ValueError(f"Attempted to delete file outside of project root: {target_path}")

    # Ensure the target is a file and exists
    if not target_path.exists():
        raise FileNotFoundError(f"No such file or directory: {target_path}")
    if target_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {target_path}")

    # Perform the deletion
    target_path.unlink()
