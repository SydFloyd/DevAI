import os

class config:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        assert self.openai_api_key is not None, "API key cannot be resolved, please check environment config"
        
        self.active_assistant_id = "asst_wfCd2yCsrNA9wmpEqgy0T1Yl"

cfg = config()