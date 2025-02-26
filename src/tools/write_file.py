"""Writes content to a specified file within a project, with sandboxing and optional linting.

This function takes a file path and content, ensuring the file is written within a specified project root directory, as defined in the configuration. It prevents writing outside the project directory or into excluded directories, and ensures the parent directory exists. If the file is a Python file, it performs linting using pylint.

Key Functions:
- `write_file`: Writes content to a file, with sandboxing and optional linting for Python files.

Notable Dependencies:
- pathlib.Path: Used for resolving and manipulating filesystem paths.
- subprocess: Utilized for running the pylint command on Python files.
- src.config.cfg: Configuration module providing project settings, such as project root and excluded directories.

Overall, this function ensures safe and controlled writing of files within a project structure, with additional linting for Python files to maintain code quality."""

from pathlib import Path
import subprocess
from src.config import cfg

def write_file(file_path: str, new_content: str, project_root: str = cfg.project_root) -> dict:
    try:
        # Resolve the full, absolute path of both project_root and the target file.
        root_path = Path(project_root).resolve()
        target_path = (root_path / file_path).resolve()

        # Check that target_path is within the project_root (basic sandboxing).
        if not str(target_path).startswith(str(root_path)):
            raise ValueError(f"Attempted to write file outside of project root: {target_path}")

        # If the target path is an existing directory, raise an error.
        if target_path.exists() and target_path.is_dir():
            raise IsADirectoryError(f"Cannot write to a directory: {target_path}")
        
        for dir in cfg.exclude_dirs:
            if str(target_path).startswith(str((root_path / dir).resolve())):
                raise PermissionError(f"Cannot write to {dir}")

        # Make sure the parent directory exists; create it if necessary.
        target_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"write_file function called, writing {len(new_content)} chars to {file_path}...")

        # Write (overwrite) the file with new_content.
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        if str(target_path).endswith(".py"):
            # After writing the file, perform linting
            lint_command = ["pylint", str(target_path)]
            lint_result = subprocess.run(lint_command, capture_output=True, text=True)

            # Return success status and linting results
            return {"success": True, "lint_output": lint_result.stdout, "lint_errors": lint_result.stderr}
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

