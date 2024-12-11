from datetime import datetime
from llama_index.core.tools import FunctionTool
import httpx
import os

async def search_web(web_query: str, brave_api_key: str | None = None) -> str:
    """Search the web using Brave API."""
    if brave_api_key is None:
        return "This is a test web search result. Please provide a Brave API key to get real search results."

    headers = {
        'X-Subscription-Token': brave_api_key,
        'Accept': 'application/json',
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            'https://api.search.brave.com/res/v1/web/search',
            params={
                'q': web_query,
                'count': 5,
                'text_decorations': True,
                'search_lang': 'en'
            },
            headers=headers
        )
        response.raise_for_status()
        data = response.json()

    results = []
    for item in data.get('web', {}).get('results', [])[:3]:
        title = item.get('title', '')
        description = item.get('description', '')
        url = item.get('url', '')
        if title and description:
            results.append(f"Title: {title}\nSummary: {description}\nSource: {url}\n")

    return "\n".join(results) if results else "No results found for the query."

# Register the tool
search_tool = FunctionTool(
    name="search_web",
    description="Search the web to answer user queries.",
    fn=search_web,
)
