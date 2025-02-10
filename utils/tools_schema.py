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


dev_tools = [
    directory_tool,
    read_file_tool,
    write_file_tool,
]