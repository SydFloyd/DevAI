from src.utils.openai_utils import OpenAIClient

DEV_INSTRUCTIONS = (
    "You are a cracked developer and software engineer.\n"
    "You pair-program with a tester who has the same toolset. You are the visionary.\n"
    "You value simple and effective solutions.\n"
    "1. Write your code to the codebase, don't send code in your messages unless you're discussing a snippet with the tester.\n"
    "2. Work together with the tester to ensure acheivement of the objective.\n"
    "3. Your environment is prepared and should be empty to start.\n"
)
TESTER_INSTRUCTIONS = (
    "You are a wise and seasoned tester.\n"
    "You pair-program with a developer who has the same toolset. You are the skeptic.\n"
    "1. Install required dependencies using the execute command tool.\n"
    "2. Run the code you're testing using the execute command tool.\n"
    "3. Test the objective, and call exit command when you have confirmed objective completion.\n"
    "4. Commands are executed in an existing venv, so no need to create or activate the venv.\n"
)

def wrap_instructs(instructions):
    return "[[[System Information]]]\n" + instructions + "[[[End System Information]]]\n\n"

class DeveloperTesterSystem:
    def __init__(self, client: OpenAIClient, developer_tools, tester_tools):
        self.client = client
        self.developer_id = self.client.create_assistant(
            name="Developer Assistant",
            assistant_instructions=DEV_INSTRUCTIONS,
            tools=developer_tools,
        )
        self.tester_id = self.client.create_assistant(
            name="Tester Assistant",
            assistant_instructions=TESTER_INSTRUCTIONS,
            tools=tester_tools,
        )
        self.developer_thread_id = self.client.create_thread()
        self.tester_thread_id = self.client.create_thread()
        
        self.objective = None

    def run(self, query):
        print("Starting developer-tester interaction...")
        if self.objective is None:
            self.objective = f"Objective: {query}"
            query = self.objective
        
        try:
            while True:
                print("Sending query to developer...")
                self.client.run_thread(wrap_instructs(DEV_INSTRUCTIONS) + query, self.developer_thread_id, self.developer_id)
                developer_response = self.client.get_latest_message(self.developer_thread_id)
                print(f"Developer response: {developer_response}")
                
                print("Sending developer response to tester...")
                self.client.run_thread(wrap_instructs(TESTER_INSTRUCTIONS) + self.objective + "\n\nDeveloper:" + developer_response, self.tester_thread_id, self.tester_id)
                if self.client.exit_flag:
                    break
                tester_response = self.client.get_latest_message(self.tester_thread_id)
                print(f"Tester response: {tester_response}")
                
                if "exit" in tester_response.lower():
                    print("Tester has approved the objective completion.")
                    break
                else:
                    print("Tester provided feedback, looping back to developer...")
                    query = tester_response  # Continue loop with tester feedback

            print("Process completed.")
        except Exception as e:
            print("Encountered error in dev-test loop:", e)
        finally:
            self.client.delete_assistant(self.developer_id)
            self.client.delete_assistant(self.tester_id)
            self.client.delete_thread(self.developer_thread_id)
            self.client.delete_thread(self.tester_thread_id)
