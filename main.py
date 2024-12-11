from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from tools.ask_user import ask_user
from tools.get_available_showtimes import get_available_showtimes
from tools.book_tickets import book_tickets
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Use the environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

tools = [
    FunctionTool.from_defaults(
        fn=ask_user,
        name="ask_user",
        description="Ask the user for additional input. The user will be prompted in the console."
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

agent = OpenAIAgent.from_tools(
    tools=tools,
    system_prompt=(
        "You are a movie booking chat assistant. Your goal is to help the user find and book movie tickets. "
        "First, ask for the movie name, their desired time, location, and the number of seats. "
        "If you need more information, use the 'ask_user' tool. "
        "When the user provides all details, use 'get_available_showtimes' to find showtimes. "
        "Offer options, and when the user selects one, use 'book_tickets' to finalize the reservation. "
        "Continue until a booking is confirmed or the user stops."
    ),
    model="gpt-4o-mini"  # Updated model
)

def main():
    print("💬 Please tell me about the movie, time, location, and number of seats you would like to book.")
    user_message = input("👉 Enter Message: ")

    while True:
        response = agent.chat(user_message)

        # Try accessing the 'response' attribute
        response_text = response.response  
        
        print(f"✨ Agent Response: {response_text}\n")
        
        if "Booking Success" in response_text:
            break
        
        user_message = input("👉 Enter Message: ")

if __name__ == "__main__":
    main()
