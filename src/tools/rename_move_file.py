"""Renames and moves a file within a specified project root directory.

This function is designed to rename and move a file from a source path to a destination path, both of which must be within a predefined project root directory. It ensures that the operation is safe by checking if the source file exists and is not a directory, and that the destination path does not already exist to prevent overwriting.

Classes/Functions:
- `rename_move_file`: Main function to rename and move a file safely within the project directory.

Notable Dependencies/Imports:
- `pathlib.Path`: Used for handling and resolving file paths.
- `src.config.cfg`: Configuration module providing the project root directory.

Overall, this function provides a secure way to handle file renaming and moving operations within a controlled environment, enforcing constraints on path locations and file existence to avoid common file handling errors."""

from pathlib import Path
from src.config import cfg

def rename_move_file(
    source_path: str,
    destination_path: str,
    project_root: str = cfg.project_root
) -> dict:
    print(f"rename_move_file called from {source_path} to {destination_path}.")

    try:
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
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

