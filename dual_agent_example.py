from src.interface.dual_agent import DeveloperTesterSystem
from src.utils.openai_utils import OpenAIClient
from src.tools_schema import dev_tools, test_tools
from src.config import cfg

dev_test = DeveloperTesterSystem(OpenAIClient(cfg.openai_api_key), dev_tools, test_tools)

query = (
    "Make a basic chess game app for play between two players. Requirements:\n"
    "1. Pieces can only move as the rules permit, including castling and en passant. \n"
    "2. A winning game is recognized. "
)

dev_test.run(query)
