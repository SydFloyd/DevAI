"""
File and directory management utilities.

This module offers a suite of functions for performing operations on files and directories, including reading, writing, deleting, renaming, and displaying directory structures. It also provides functionality to extract docstrings from Python files, making it useful for development and file manipulation tasks.

Functions:
    - build_directory_tree: Displays the directory tree of the project directory.
    - read_file(file_path: str) -> str: Reads the contents of a file at the specified path.
    - write_file(file_path: str, new_content: str): Writes or overwrites a file with new content.
    - delete_file(file_path: str): Deletes a file at the specified file path.
    - rename_move_file(source_path: str, destination_path: str): Renames or moves a file from a source path to a destination path.
    - read_docstring(file_path: str) -> str: Reads the top-level docstring from a given Python file.
"""

directory_tool = {
    "type": "function",
    "function": {
        "name": "build_directory_tree",
        "description": "See the directory tree of the project directory."
    }
}

read_file_tool = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "read contents of a file at file_path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path of file to be read"
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        },
        "strict": True
    }
}

write_file_tool = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites a file with new content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to be written or overwritten."
                },
                "new_content": {
                    "type": "string",
                    "description": "The new content to write into the file."
                }
            },
            "required": ["file_path", "new_content"],
            "additionalProperties": False
        },
        "strict": True
    }
}

delete_file_tool = {
    "type": "function",
    "function": {
        "name": "delete_file",
        "description": "Deletes a file at the specified file path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to be deleted."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        },
        "strict": True
    }
}

rename_move_file_tool = {
    "type": "function",
    "function": {
        "name": "rename_move_file",
        "description": "Renames or moves a file from source_path to destination_path.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path of the file to be moved or renamed."
                },
                "destination_path": {
                    "type": "string",
                    "description": "The new path for the file."
                }
            },
            "required": ["source_path", "destination_path"],
            "additionalProperties": False
        },
        "strict": True
    }
}

read_docstring_tool = {
    "type": "function",
    "function": {
        "name": "read_docstring",
        "description": "Reads the top-level docstring from a given Python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the Python file to read the docstring from."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        },
        "strict": True
    }
}


dev_tools = [
    directory_tool,
    read_file_tool,
    write_file_tool,
    delete_file_tool,
    rename_move_file_tool,
    read_docstring_tool,
]


