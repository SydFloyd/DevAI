"""
main.py

This module provides the main entry point for the client interaction system using the OpenAI utilities. 
It handles the execution of dynamically loaded tools, processes user inputs, and manages interactions through a client-server model. 
Key functions in this module facilitate the execution of configured tools and provide a loop for continuous user interaction.

Functions:
- execute_tools(run): Executes tool functions based on the 'run' configuration and returns the tool outputs.
- submit_tools_and_get_run(run, tool_outputs, thread_id): Submits the results of tool execution to the client and polls for updates on the run status.
- interact(assistant_id, thread_id): Manages the interactive session, collecting user input and coordinating tool execution.
- output_messages(run, thread_id): Outputs messages from the completed interaction session.
- engage(assistant_id): Initiates and maintains an interactive session loop with a given assistant configuration.
- main(): Sets up and initializes the assistant interaction using configuration settings from 'cfg'.

This module requires the 'src.openai_utils' and 'src.config.cfg' to provide necessary configurations and utilities for client interactions.
"""

from src.openai_utils import *
from src.config import cfg
import importlib
import json

client = get_client()

def execute_tools(run):
    tool_outputs = []
    if hasattr(run, "required_action"):
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            function_name = tool.function.name
            function_args = tool.function.arguments
            try:
                tools_module = importlib.import_module(f"src.tools.{function_name}")
                tool_function = getattr(tools_module, function_name)
                if isinstance(function_args, str):
                    function_args = json.loads(function_args)  # Convert string to dict
                output = tool_function(**function_args)
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": str(output)  # Convert output to string if necessary
                })
            except Exception as e:
                print(f"Error executing {function_name}: {e}")
    return tool_outputs

def submit_tools_and_get_run(run, tool_outputs, thread_id):
    try:
        return client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    except Exception as e:
        print("Failed to submit tool outputs:", e)
        return run

def interact(assistant_id, thread_id):
    query = input(f"\n{cfg.agent_name}>> ")
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=query,
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while run.status == 'requires_action':
        tool_outputs = execute_tools(run)
        if tool_outputs:
            run = submit_tools_and_get_run(run, tool_outputs, thread_id)
            print("Tool outputs submitted successfully.")
        else:
            print("No tool outputs to submit.")
            break

    output_messages(run, thread_id)

def output_messages(run, thread_id):
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for message in messages:
            print(message.role + ":")
            for c in message.content:
                print(c.text.value)
            break
    else:
        print(run.status)

def engage(assistant_id):
    assistant_id = create_assistant()
    thread = client.beta.threads.create()
    try:
        while True:
            interact(assistant_id, thread.id)
    finally:
        delete_assistant(assistant_id)

def main():
    print("Using assistant_id:", cfg.active_assistant_id)
    engage(cfg.active_assistant_id)

if __name__ == "__main__":
    main()
