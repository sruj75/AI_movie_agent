from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from tools.web_search import search_web, WebSearchDeps
from dotenv import load_dotenv
import asyncio
import os
from httpx import AsyncClient
from tenacity import retry, wait_exponential, stop_after_attempt

# Load environment variables from .env file
load_dotenv()

# Use the environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

async def web_search_wrapper(web_query: str) -> str:
    """Wrapper function to make the async web search work with LlamaIndex"""
    async with AsyncClient() as client:
        brave_api_key = os.getenv('BRAVE_API_KEY', None)
        deps = WebSearchDeps(client=client, brave_api_key=brave_api_key)
        return await search_web(deps, web_query)

# Create a synchronous version for LlamaIndex
def web_search_sync(web_query: str) -> str:
    return asyncio.run(web_search_wrapper(web_query))

# Define tools
tools = [
    FunctionTool.from_defaults(
        fn=web_search_sync,
        name="web_search",
        description="Search the web for current information about a topic"
    )
]

# Create the agent
agent = OpenAIAgent.from_tools(
    tools=tools,
    system_prompt=(
        "You are an expert at researching the web to answer user questions. "
        "Use the web_search tool to find relevant and up-to-date information. "
        "Always cite your sources and provide clear, concise answers."
    ),
    model="gpt-4"  # You can adjust the model as needed
)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def get_agent_response(user_message: str):
    return agent.chat(user_message)

def main():
    print("💬 Ask me anything, and I'll search the web for answers!")
    user_message = input("👉 Enter Message: ")

    while True:
        response = agent.chat(user_message)
        response_text = response.response
        print(f"✨ Agent Response: {response_text}\n")
        
        user_message = input("👉 Enter Message (or 'quit' to exit): ")
        if user_message.lower() == 'quit':
            break

if __name__ == "__main__":
    main()