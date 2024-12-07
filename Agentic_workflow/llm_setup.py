import os
import openai
from llama_index import SimpleDirectoryReader, VectorStoreIndex, LLMPredictor, ServiceContext
from llama_index import LLMAgent, Tool
from Agentic_workflow.agent_tools import check_showtimes_tool, book_tickets_tool
from llama_index.llms import OpenAI
from llama_index.agent import PlanAndExecute, load_agent_executor, load_agent_planner
from supabase import create_client
from llama_index.core.schema import Document

openai.api_key = os.environ.get("OPENAI_API_KEY")

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Fetch data from Supabase
response = supabase.table('movies').select("*").execute()
movies_data = response.data

# Fetch movies and their showtimes from Supabase
documents = []
for movie in movies_data:
    # First get showtimes for this movie
    showtimes_response = supabase.table('showtimes').select("*").eq('movie_id', movie['id']).execute()
    showtimes_data = showtimes_response.data
    
    # Format showtimes information
    formatted_showtimes = []
    for showtime in showtimes_data:
        formatted_showtimes.append(
            f"Showtime: {showtime['name']}\n"
            f"Time: {showtime['show_time']}\n"
            f"Available Seats: Balcony: {showtime['balcony_seats']}, "
            f"First Class: {showtime['first_class_seats']}"
        )
    
    # Create comprehensive movie document with all details
    content = f"""
    Movie: {movie['title']}
    Year: {movie['year']}
    IMDB ID: {movie['imdb_id']}
    Poster URL: {movie['poster_url']}
    
    Available Showtimes:
    {'-' * 40}
    {'\n'.join(formatted_showtimes) if formatted_showtimes else 'No showtimes available'}
    
    Additional Information: {movie.get('additional_info', {})}
    """
    
    doc = Document(text=content)
    documents.append(doc)

# Create the index directly from the Supabase data
index = VectorStoreIndex.from_documents(documents)

llm_predictor = LLMPredictor(llm=OpenAI(model="gpt-4", temperature=0))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

tools = [
    {
        "function": check_showtimes_tool,
        "name": "check_showtimes",
        "description": "Check available showtimes for a given movie name."
    },
    {
        "function": book_tickets_tool,
        "name": "book_tickets",
        "description": "Book tickets for a given movie, showtime, and number of seats."
    },
]

system_prompt = """You are a helpful movie booking assistant. 
When the user asks a question, first break down the request into a series of steps (a plan). 
Then execute those steps one by one. If you need information from the database (which is indexed by LlamaIndex), query the index. 
If you need to check showtimes or book tickets, use the provided tools.

Follow this process:
1. Think about what the user wants and create a step-by-step plan.
2. Execute the plan step-by-step. If you need to call a tool, call it. If you need information, query the index.
3. After completing the steps, summarize and provide the answer to the user.

Be explicit in your reasoning, but only show the user the final answer. Do not reveal the hidden reasoning steps.
"""

planner = load_agent_planner(llm_predictor)
executor = load_agent_executor(tools, llm_predictor)

agent = PlanAndExecute(
    planner=planner,
    executor=executor,
    index=index,
    system_prompt=system_prompt,
    service_context=service_context,
    verbose=True
) 