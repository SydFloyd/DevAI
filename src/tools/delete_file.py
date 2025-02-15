from pathlib import Path

def delete_file(file_path: str, project_root: str = ".") -> dict:
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
