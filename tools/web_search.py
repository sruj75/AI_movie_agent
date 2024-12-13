import os
import asyncio
from typing import Any
import logfire
from httpx import AsyncClient
from dataclasses import dataclass

@dataclass
class WebSearchDeps:
    client: AsyncClient
    brave_api_key: str | None

async def _async_search_web(web_query: str) -> str:
    """Async implementation of web search"""
    async with AsyncClient() as client:
        brave_api_key = os.getenv('BRAVE_API_KEY', None)
        
        if brave_api_key is None:
            return "This is a test web search result. Please provide a Brave API key to get real search results."

        headers = {
            'X-Subscription-Token': brave_api_key,
            'Accept': 'application/json',
        }
        
        with logfire.span('calling Brave search API', query=web_query) as span:
            r = await client.get(
                'https://api.search.brave.com/res/v1/web/search',
                params={
                    'q': web_query,
                    'count': 5,
                    'text_decorations': True,
                    'search_lang': 'en'
                },
                headers=headers
            )
            r.raise_for_status()
            data = r.json()
            span.set_attribute('response', data)

        results = []
        
        # Add web results in a nice formatted way
        web_results = data.get('web', {}).get('results', [])
        for item in web_results[:3]:
            title = item.get('title', '')
            description = item.get('description', '')
            url = item.get('url', '')
            if title and description:
                results.append(f"Title: {title}\nSummary: {description}\nSource: {url}\n")

        return "\n".join(results) if results else "No results found for the query."

def search_web(web_query: str) -> str:
    """
    Synchronous wrapper for web search to be used with LlamaIndex tools.
    
    Args:
        web_query: The search query string
        
    Returns:
        str: Formatted search results
    """
    return asyncio.run(_async_search_web(web_query))
