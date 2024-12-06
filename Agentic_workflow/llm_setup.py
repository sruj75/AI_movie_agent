import os
import openai
from llama_index import SimpleDirectoryReader, VectorStoreIndex, LLMPredictor, ServiceContext
from llama_index import LLMAgent, Tool
from Agentic_workflow.agent_tools import check_showtimes_tool, book_tickets_tool
from llama_index.llms import OpenAI
from llama_index.agent import PlanAndExecute, load_agent_executor, load_agent_planner

openai.api_key = os.environ.get("OPENAI_API_KEY")

documents = SimpleDirectoryReader("./").load_data(files=["movies_data.txt"])
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
    service_context=service_context
) 