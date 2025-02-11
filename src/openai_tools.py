from openai import OpenAI

def get_client():
	try:
		with open("local/key.txt", "r") as f:
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

	INSTRUCTIONS = (
		"You are a senior software developer, a 10x engineer, a f**king wizard. \n"
		"You have access to tools for reading and writing to a codebase. \n"
		"The codebase you are working on is the one through which we are interacting. \n"
		"Reflect on your experience, in terms of what information you can see, and what information would be useful for you to see. \n"
		"You are free to make modifications to the code that make our interaction more smooth. \n"
		"Currently, we've been focusing on making the codebase more readable and scalable for ease of development, then we will expand/refine your toolset."
		"Please let me know how I can help.  I look forward to working together."
	)

	assistant = client.beta.assistants.create(
		instructions=INSTRUCTIONS,
		name="Developer of DevAI",
		tools=[{"type": "code_interpreter"}, *dev_tools],
		model="gpt-4o",
	)

	print(f"Created assistant {assistant.id}")

if __name__ == "__main__":
	create_assistant()