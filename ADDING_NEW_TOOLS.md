# Adding New Tools

To add a new tool to the project, follow these steps:

1. **Create the Tool Script:**
   - Implement your tool as a Python script under the `src/tools/` directory.
   - Ensure your tool has a clear purpose, and implement it in a single function.
   - **Important**: The function name within the script must match the script name for dynamic execution. Example:
     - Script name: `my_tool_script.py`
     - Function name: `def my_tool_script(params):`

2. **Import the Tool:**
   - Update the `src/tools/__init__.py` file to import the new tool function.
     ```python
     from .my_tool_script import my_tool_script
     ```

3. **Define the Tool Schema:**
   - Update `src/tools_schema.py` to include a new dictionary entry for your tool, specifying its function name, description, and parameters.
     ```python
     my_tool_schema = {
         "type": "function",
         "function": {
             "name": "my_tool_script",
             "description": "Description of what the tool does.",
             "parameters": {
                 "type": "object",
                 "properties": {
                     "param_name": {
                         "type": "param_type",
                         "description": "Parameter description."
                     }
                 },
                 "required": ["param_name"],
                 "additionalProperties": False
             },
             "strict": True
         }
     }
     ```

4. **Add to the Tools List:**
   - Include your new tool definition in the `dev_tools` list within `tools_schema.py`.

5. **Testing:**
   - Make sure to test your tool to ensure it integrates smoothly with the rest of the toolset.

By following these steps, you can expand the functionality of the project with custom tool integrations.
