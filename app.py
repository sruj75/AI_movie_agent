import asyncio
import os
from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import httpx
import logfire
from dataclasses import dataclass
from tools.ask_user import ask_user
from tools.get_available_showtimes import get_available_showtimes
from tools.book_tickets import book_tickets
from tools.web_search import search_web

# Configure logging and env
logfire.configure(send_to_logfire='if-token-present')
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

@dataclass
class Deps:
    client: httpx.AsyncClient
    brave_api_key: str | None

# Configure OpenAI LLM
llm = OpenAI(
    model="gpt-4o-mini",
    streaming=True
)

# Create all tools
tools = [
    FunctionTool.from_defaults(
        fn=lambda *args, **kwargs: asyncio.run(search_web(*args, **kwargs)),
        name="search_web",
        description="Search the web for movie information and reviews.",
    ),
    FunctionTool.from_defaults(
        fn=ask_user,
        name="ask_user",
        description="Ask the user for additional input about movie booking."
    ),
    FunctionTool.from_defaults(
        fn=get_available_showtimes,
        name="get_available_showtimes",
        description="Get available showtimes for a given movie, location, and seat requirement."
    ),
    FunctionTool.from_defaults(
        fn=book_tickets,
        name="book_tickets",
        description="Book seats for a showtime."
    )
]

# Create the unified agent
agent = OpenAIAgent.from_tools(
    tools=tools,
    llm=llm,
    system_prompt=(
        "You are a movie assistant that can both search for movie information and help book tickets. "
        "If the user asks about movie information, reviews, or details, use the search_web tool. "
        "If they want to book tickets, help them by asking for movie name, time, location, and seats using ask_user tool. "
        "Use get_available_showtimes to check availability and book_tickets to complete the booking. "
        f"The current date is: {datetime.now().strftime('%Y-%m-%d')}."
    ),
)

async def prompt_ai(prompt: str, brave_api_key: str):
    """Stream responses from the agent."""
    # Pass the brave_api_key as a direct parameter
    response = await agent.stream_chat(
        prompt,
        function_kwargs={"search_web": {"brave_api_key": brave_api_key}}  # Specify which function gets which kwargs
    )
    
    async for chunk in response:
        yield chunk.response

async def main():
    st.title("Movie Information & Booking Assistant")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous messages
    for message in st.session_state.messages:
        role, content = message
        with st.chat_message(role):
            st.markdown(content)

    if prompt := st.chat_input("Ask about movies or book tickets"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append(("user", prompt))

        response_content = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            brave_api_key = os.getenv("BRAVE_API_KEY", None)

            async for chunk in prompt_ai(prompt, brave_api_key):
                response_content += chunk
                message_placeholder.markdown(response_content)

        st.session_state.messages.append(("assistant", response_content))

if __name__ == "__main__":
    asyncio.run(main()) 