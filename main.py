from src.utils.dev_tester import DeveloperTesterSystem
from src.utils.openai_utils import OpenAIClient
from src.tools_schema import dev_tools, test_tools
from src.config import cfg

dev_test = DeveloperTesterSystem(OpenAIClient(cfg.openai_api_key), dev_tools, test_tools)

# query = "Train a NN to balance a simulated swinging arm upright.  Review the existing foundation code and iterate until the model is successful.  Use pytorch, not tensorflow."
query = "Given the existing codebase which is for training an NN to balance a swinging arm upright, create a script that lets a user run the simulation with some keybindings for the actions."

dev_test.run(query)
