import asyncio
import os
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from web_search_agent import search_tool
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure OpenAI LLM
llm = OpenAI(
    model="gpt-4o-mini",
    # api_key="some key",  # uses OPENAI_API_KEY env var by default
)

# Create the agent with the web search tool
web_search_agent = OpenAIAgent.from_tools(
    tools=[search_tool],
    llm=llm,
    system_prompt=(
        "You are an expert at researching the web to answer user questions. "
        f"The current date is: {datetime.now().strftime('%Y-%m-%d')}."
    ),
)

async def prompt_ai(prompt: str, brave_api_key: str) -> str:
    """Run the web search agent with a prompt."""
    response = await web_search_agent.chat(prompt, tool_kwargs={"brave_api_key": brave_api_key})
    return response.response  # Access the response attribute

async def main():
    st.title("LlamaIndex AI Chatbot (Web Search)")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        role, content = message
        with st.chat_message(role):
            st.markdown(content)

    # React to user input
    if prompt := st.chat_input("What would you like to research today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(("user", prompt))

        # Display assistant response in chat message container
        response_content = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            brave_api_key = os.getenv("BRAVE_API_KEY", None)

            # Generate a response and update the UI dynamically
            response_content = await prompt_ai(prompt, brave_api_key)
            message_placeholder.markdown(response_content)

        st.session_state.messages.append(("assistant", response_content))

if __name__ == "__main__":
    asyncio.run(main())
