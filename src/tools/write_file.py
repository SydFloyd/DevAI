from pathlib import Path

def write_file(file_path: str, new_content: str, project_root: str = ".") -> None:
    """
    Overwrites (or creates) a file in the given project root with new_content.
    
    :param file_path: Path to the file to be written (can be relative to project_root).
    :param new_content: The string content to write to the file.
    :param project_root: The root directory within which the file must be written.
    :raises ValueError: If the resolved file path is outside the project_root.
    :raises IsADirectoryError: If the path is a directory.
    """
    print(f"write_file function called, wrote {len(new_content)} chars to {file_path}.")
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
