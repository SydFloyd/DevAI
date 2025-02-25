"""
Module for generating structured documentation summaries of a codebase.

This module provides functions to recursively analyze Python files in a directory, generate summaries for each file, and compile these into folder-level and codebase-level documentation. It leverages a language model to create concise and informative summaries of code components and their interactions.

Functions:
    - generate_file_summaries(client, root_dir): Summarizes each Python file in the specified directory.
    - generate_subfolder_summaries(client, file_summaries): Produces summaries for each folder based on file summaries.
    - generate_root_summary(client, intermediate_summaries): Compiles folder summaries into a comprehensive codebase summary.
    - document_codebase(root_dir): Orchestrates the generation of the entire codebase documentation.
    - save_codebase_doc(): Saves the generated documentation to a markdown file.
"""

import os
from src.config import cfg
from src.utils.openai_utils import get_client, chat

def generate_file_summaries(client, root_dir):
    """
    Walks through all files in `root_dir`,
    calls your LLM summarizer for each file,
    and stores the result in a dictionary keyed by file path.
    """
    file_summaries = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in cfg.exclude_dirs]
        for file in filenames:
            if file.endswith(".py"):
                filepath = os.path.join(dirpath, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    code_content = f.read()

                prompt = (
                    "Provide a structured summary of the below module.\n"
                    " - Key classes/functions and their roles\n"
                    " - Notable dependencies/imports\n"
                    " - Overall purpose and functionality\n"
                    "Include only the summary in your response and no other information; the summary will be used programmatically."
                    "Module code:\n\n"
                    f"{code_content}"
                )
                
                print(f"Summarizing {filepath} ({len(code_content)} chars)...")
                summary = chat(client, prompt, system_message="You are an expert in generating complete and concise documentation of code.")
                
                file_summaries[filepath] = summary

    return file_summaries


def generate_subfolder_summaries(client, file_summaries):
    """
    Given a dict of file_summaries keyed by filepath,
    group by immediate parent directory and produce a summary
    for each.
    """
    from collections import defaultdict

    folder_summaries = defaultdict(list)

    for filepath, summary in file_summaries.items():
        folder_path = os.path.dirname(filepath)
        folder_summaries[folder_path].append("```" + filepath + ":\n" + summary + "\n```")

    intermediate_summaries = {}
    for folder_path, summaries in folder_summaries.items():
        # If the repos get too big, we'll have to chunk this
        joined_summaries = "\n\n".join(summaries)

        prompt = (
            "Combine the below file-level docs into a cohesive summary of the folder:\n"
            "- Overall functionality and architecture\n"
            "- Notable interactions among files\n"
            "- Key classes, functions, or patterns\n"
            f"{joined_summaries}"
        )

        print(f"Reducing summaries for {folder_path} ({len(summaries)} file summaries - {len(joined_summaries)} chars)...")
        reduced_summary = chat(client, prompt, system_message="You are an expert in generating complete and concise documentation of code.")

        intermediate_summaries[folder_path] = reduced_summary

    return intermediate_summaries


def generate_root_summary(client, intermediate_summaries):
    """
    Takes a dictionary of {folder_path: summary} for top-level folders
    and merges them into a single 'master doc' for the codebase.
    """
    joined_folder_summaries = "\n\n".join(intermediate_summaries.values())

    prompt = (
        "You are creating a top-level doc for the entire codebase given the below summaries.\n"
        "- Summarize the main components/folders\n"
        "- Describe the overarching architecture\n"
        "- Note the primary dependencies between major sub-systems\n"
        "- Keep it concise yet comprehensive\n"
        f"{joined_folder_summaries}"
    )
    
    print(f"Generating final doc ({len(intermediate_summaries)} intermediate summaries - {len(intermediate_summaries)} chars)...")
    codebase_summary = chat(client, prompt, system_message="You are an expert in generating complete and concise documentation of code.")

    return codebase_summary


def document_codebase(root_dir):
    client = get_client()
    file_summaries = generate_file_summaries(client, root_dir=root_dir)
    subfolder_summaries = generate_subfolder_summaries(client, file_summaries=file_summaries)
    codebase_summary = generate_root_summary(client, intermediate_summaries=subfolder_summaries)

    return codebase_summary


def save_codebase_doc():
    documentation = document_codebase(cfg.project_root)
    with open("docs.md", 'w') as f:
        f.write(documentation)

