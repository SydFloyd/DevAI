from openai import OpenAI

def get_client():
	try:
		with open("key.txt", "r") as f:
			openai_key = f.read().strip()
		assert openai_key != None
	except:
		raise ValueError("Couldn't resolve openai api key")

	client = OpenAI(
		api_key = openai_key
	)

	return client

def create_assistant():
	'''New assistant is created whenever toolset is expanded.'''

	from utils.tools_schema import dev_tools

	client = get_client()

	assistant = client.beta.assistants.create(
		instructions="You are a senior software developer, a 10x engineer, a f**king wizard.",
		name="Developer",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o",
	)

	print(f"Created assistant {assistant.id}")

def create_thread():
	client = get_client()
	