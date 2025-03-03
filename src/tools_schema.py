"""This module provides a collection of tools designed to perform various file and directory operations as well as command execution tasks. It includes functionalities to build directory trees, read and write file contents, delete and rename files, and execute system commands. The main components are:

- `build_directory_tree`: A function to generate and view the directory tree of a specified project directory.

- `read_file`: A function to read the contents of a file given its path. It requires the parameter `file_path` which specifies the location of the file to be read.

- `write_file`: A function that writes or overwrites a file with new content. If the file is a Python file, it automatically returns linting information. It requires `file_path` and `new_content` parameters.

- `delete_file`: A function to delete a file at a specified path. It requires the `file_path` parameter.

- `rename_move_file`: A function to rename or move a file from a source path to a destination path. It requires `source_path` and `destination_path` parameters.

- `read_docstring`: A function to read the top-level docstring from a given Python file. It requires the `file_path` parameter.

- `execute_command`: A function to execute a command on the machine after obtaining user approval. It requires the `command` parameter.

These tools collectively facilitate file management and command execution, making them useful for development and scripting tasks."""

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
        "description": "Writes or overwrites a file with new content. Returns linting info for .py files automatically.",
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

execute_command_tool = {
    "type": "function",
    "function": {
        "name": "execute_command",
        "description": "Executes a command on the Windows machine.  Requires user approval.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute on the Windows machine."
                }
            },
            "required": ["command"],
            "additionalProperties": False
        },
        "strict": True
    }
}

exit_tool = {
    "type": "function",
    "function": {
        "name": "exit",
        "description": "Call this function when you have tested and confirmed the developer's results.",
        "parameters": {
            "type": "object",
            "properties": {
                "test_summary": {
                    "type": "string",
                    "description": "Your final test summary report."
                }
            },
            "required": ["test_summary"],
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
    execute_command_tool,
]

test_tools = [
    exit_tool,
    execute_command_tool,
    read_file_tool,
    write_file_tool,
    delete_file_tool,
    rename_move_file_tool,
    directory_tool,
]
