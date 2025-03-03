from src.utils.dev_tester import DeveloperTesterSystem
from src.utils.openai_utils import OpenAIClient
from src.tools_schema import dev_tools, test_tools
from src.config import cfg

dev_test = DeveloperTesterSystem(OpenAIClient(cfg.openai_api_key), dev_tools, test_tools)

query = "Create a basic demonstration of machine learning classification problem.  Use a classic dataset, but not iris."

dev_test.run(query)
