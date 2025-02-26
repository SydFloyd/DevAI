"""Reads and returns the module-level docstring of a Python file within a specified project root.

This function attempts to read the module-level docstring from a Python file specified by `file_path`, ensuring that the file is located within the given `project_root`, which defaults to a configured project root directory. It uses the `ast` module to parse the file and extract the docstring, if present.

Key elements:
- `read_docstring`: Main function that performs the operations described above.
- Dependencies: 
  - `pathlib.Path`: Used for handling and resolving file paths.
  - `ast`: Utilized to parse the Python file and retrieve the docstring.
  - `src.config.cfg`: Provides the default project root directory.

Returns a dictionary containing the docstring under the "docstring" key, or an "error" key with a descriptive message if any issue arises during the process, such as file not found, path being a directory, or access outside the project root."""

from pathlib import Path
import ast
from src.config import cfg

def read_docstring(file_path: str, project_root: str = cfg.project_root) -> dict:
    print(f"read_docstring function called on {file_path}.")
    
    try:
        # Resolve the full, absolute path of both project_root and the target file.
        root_path = Path(project_root).resolve()
        target_path = (root_path / file_path).resolve()

        # Check that target_path is within the project_root.
        if not str(target_path).startswith(str(root_path)):
            raise ValueError(f"Attempted to access file outside of project root: {target_path}")

        # Ensure the target is a file and exists.
        if not target_path.exists():
            raise FileNotFoundError(f"No such file or directory: {target_path}")
        if target_path.is_dir():
            raise IsADirectoryError(f"Path is a directory, not a file: {target_path}")

        # Extract the docstring using the ast module.
        with open(target_path, "r", encoding="utf-8") as f:
            module_ast = ast.parse(f.read(), filename=str(target_path))
        
        # Return the docstring if available.
        return {"docstring": ast.get_docstring(module_ast) or ""}
    except Exception as e:
        return {"error": str(e)}

