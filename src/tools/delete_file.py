"""This module provides functionality to delete a specified file from the project's directory structure. It ensures that file deletions occur only within the designated project root directory, enhancing security by preventing accidental or malicious deletions outside the intended scope.

Key Function:
- `delete_file(file_path: str, project_root: str = cfg.project_root) -> dict`: Attempts to delete the file specified by `file_path` relative to the `project_root`. Returns a dictionary indicating success or details of any error encountered.

Notable Dependencies:
- `pathlib.Path`: Utilized for file path manipulations and to ensure cross-platform compatibility.
- `src.config.cfg`: Imported configuration object that provides the default project root directory path. 

The function ensures that the target path is a file, exists, and lies within the project root before performing the deletion. It handles various exceptions to provide informative error messages in the return dictionary."""

from pathlib import Path
from src.config import cfg

def delete_file(file_path: str, project_root: str = cfg.project_root) -> dict:
    print(f"delete_file function called on {file_path}.")
    root_path = Path(project_root).resolve()
    target_path = (root_path / file_path).resolve()

    try:
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
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

