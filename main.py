from src.openai_tools import *
import importlib
import json

client = get_client()

def interact(assistant_id, thread_id):
    query = input(f"\nDeveloper Assistant>>")

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
        tool_outputs = []
        
        if hasattr(run, "required_action"):
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool.function.name 
                function_args = tool.function.arguments 

                try:
                    tools_module = importlib.import_module("src.utils.tools_functions")
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
        
        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")
            break

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for message in messages:
            print(message.role + ":")
            for c in message.content:
                print(c.type + ": ", c.text.value)
            break
    else:
        print(run.status)

def engage(assistant_id):
    thread = client.beta.threads.create()

    while True:
        interact(assistant_id, thread.id)

def main():
    assistant_id = "asst_ESqlAIO8s3GxJi0oQxf9ldrE"
    engage(assistant_id)

if __name__ == "__main__":
    main()