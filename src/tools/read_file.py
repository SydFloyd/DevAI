from pathlib import Path

def read_file(file_path: str, project_root: str = ".") -> dict:
    print(f"read_file function called on {file_path}.")
    try:
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

        # Read and return the file's contents.
        with open(target_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}

    except Exception as e:
        return {"error": str(e)}

