import os
from llama_index import OpenAIAgent
from tools.ask_user import ask_user
from tools.get_available_showtimes import get_available_showtimes
from tools.book_tickets import book_tickets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

tools = [
    {
        "name": "ask_user",
        "description": "Ask the user for additional input.",
        "fn": ask_user,
        "fn_schema": {
            "name": "ask_user",
            "description": "Ask the user a question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_prompt": {
                        "type": "string",
                        "description": "Prompt to display."
                    }
                },
                "required": ["input_prompt"]
            }
        }
    },
    {
        "name": "get_available_showtimes",
        "description": "Check for available movie showtimes.",
        "fn": get_available_showtimes,
        "fn_schema": {
            "name": "get_available_showtimes",
            "description": "Find showtimes near a requested time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_name": {"type": "string"},
                    "location": {"type": "string"},
                    "seats_needed": {"type": "integer"},
                    "desired_time": {"type": "string"}
                },
                "required": ["movie_name", "location", "seats_needed", "desired_time"]
            }
        }
    },
    {
        "name": "book_tickets",
        "description": "Book seats for a showtime.",
        "fn": book_tickets,
        "fn_schema": {
            "name": "book_tickets",
            "description": "Books specified seats for a movie showtime.",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_name": {"type": "string"},
                    "location": {"type": "string"},
                    "time": {"type": "string"},
                    "seats_to_book": {"type": "integer"},
                    "reservation_name": {"type": "string"}
                },
                "required": ["movie_name", "location", "time", "seats_to_book", "reservation_name"]
            }
        }
    }
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
    model="gpt-4-0613"  # or gpt-3.5-turbo-0613
)

def main():
    print("💬 Please tell me about the movie, time, location, and number of seats you’d like to book.")
    user_message = input("👉 Enter Message: ")

    while True:
        response = agent.chat(user_message)
        print(f"✨ Agent Response: {response}\n")
        
        # Check if the response indicates a finished booking
        if "Booking Success" in response:
            break
        
        user_message = input("👉 Enter Message: ")

if __name__ == "__main__":
    main()
