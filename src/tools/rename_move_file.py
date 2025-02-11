from pathlib import Path

def rename_move_file(
    source_path: str,
    destination_path: str,
    project_root: str = "."
) -> None:
    """
    Renames or moves a file from source_path to destination_path within the project_root sandbox.

    :param source_path: The path to the file to be moved or renamed.
    :param destination_path: The new path for the file.
    :param project_root: The root directory within which the operation should occur.
    :raises ValueError: If the resolved paths are outside the project_root.
    :raises FileNotFoundError: If the source file does not exist.
    :raises FileExistsError: If the destination file already exists.
    :raises IsADirectoryError: If the source is not a file.
    """
    print(f"rename_move_file called from {source_path} to {destination_path}.")

    root_path = Path(project_root).resolve()
    source = (root_path / source_path).resolve()
    destination = (root_path / destination_path).resolve()

    # Check if paths are within the project root
    if not str(source).startswith(str(root_path)) or not str(destination).startswith(str(root_path)):
        raise ValueError(f"Attempted to operate outside of project root: {source}, {destination}")

    # Ensure the source is a file and exists
    if not source.exists():
        raise FileNotFoundError(f"Source file does not exist: {source}")
    if source.is_dir():
        raise IsADirectoryError(f"Source is a directory, not a file: {source}")

    # Ensure the destination does not already exist to prevent overwriting
    if destination.exists():
        raise FileExistsError(f"Destination file already exists: {destination}")

    # Perform the move/rename operation
    source.rename(destination)
