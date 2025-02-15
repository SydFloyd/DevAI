"""
Tools for file and directory management operations.

This module provides a set of functions to perform various file and directory operations such as reading, writing, deleting, and renaming files, as well as building directory trees and reading docstrings from Python files.

Functions:
    - build_directory_tree: Displays the directory tree of the project directory.
    - read_file: Reads the contents of a file at a specified path.
    - write_file: Writes or overwrites a file with new content.
    - delete_file: Deletes a file at the specified file path.
    - rename_move_file: Renames or moves a file from a source path to a destination path.
    - read_docstring: Reads the top-level docstring from a given Python file.
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
