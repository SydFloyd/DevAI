from pydantic import BaseModel
from src.utils.openai_utils import OpenAIClient
from src.config import cfg

class Task(BaseModel):
    name: str
    description: str

class TaskBreakdown(BaseModel):
    tasks: list[Task]

class ProjectManager:

    def __init__(self):
        self.client = OpenAIClient(api_key=cfg.openai_api_key)

    def _build_outline(self, query):
        system_message = "You are an expert in system architect and design."
        prompt = (
            "Given the subject below, outline a complete solution.\n"
            "1. The solution will be a codebase built from scratch, and not require the use of consumer software, unless it can be incorperated into a system.\n"
            "2. Do not ask the user any clarifying questions, as your response is interpreted programmatically.\n"
            "3. Fill in any gaps with your best judgement, prioritizing simple, feasibly, and functional solutions.\n"
            f"Subject: {query}"
        )
        self.outline = self.client.chat(prompt, system_message=system_message)
    
    def _break_down_tasks(self):
        system_message = "You are an expert project manager, able to breakdown a project into chunks of just the right size."
        prompt = (
            "Break down the project below into tasks. The tasks should be sized optimally to reduce dependencies bewteen tasks in development.\n"
            "1. Tasks should focus on development tasks contributing to the core project, not testing, version control.\n"
            "2. Ideally, each task represents a module of the system.\n"
            "3. Ensure each task contributes to the core project below, avoiding creating unecessary tasks.\n"
            "4. Tasks must be able to be completed using only text-base system interaction.\n"
            f"Project outline:\n\n{self.outline}"
        )
        self.tasks = self.client.chat(prompt, system_message=system_message, response_format=TaskBreakdown)
    
    def run(self, query):
        self._build_outline(query)
        self._break_down_tasks()
        return self.outline, self.tasks
