from src.utils.dev_tester import DeveloperTesterSystem
from src.utils.openai_utils import OpenAIClient
from src.tools_schema import dev_tools, test_tools
from src.config import cfg

dev_test = DeveloperTesterSystem(OpenAIClient(cfg.openai_api_key), dev_tools, test_tools)

# query = (
#     "Create a basic game replicating the 'slap game'. "
#     "The game traditionally involves 2 player, one on offense, the other on defense. "
#     "The players start with their hands touching, palms facing. "
#     "The offensive player's palms up, with defense's palms down. "
#     "The offensive player must slap one or both of the defensive players hands. "
#     "The defensive player must remove their hand before it is slapped. \n"
#     "If the offensive player misses, they lose a point. "
#     "The defensive player loses 1 point per hand slapped. "
#     "If the defensive player removes their hand completely from the other player's hand, they lose 1 point (per hand).\n\n"
#     "The POC of this game can be based in a command terminal, where hands are represented by some abstract shape. "
#     "There should be a range of motion for both the slap and the 'block' (defensive move); "
#     "that way we can set a threshold of what's considered an attempted slap or 'block'."
# )

query = (
    "Make a basic chess game app for play between two players. Requirements:\n"
    "1. Pieces can only move as the rules permit, including castling and en passant. \n"
    "2. A winning game is recognized. "
    )


dev_test.run(query)
