from typing import Any, List, Dict, Optional, Union
import asyncio
import logging

from mcp.server.fastmcp import FastMCP
from web_search import search, advanced_search
from scholarly import scholarly


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mcp = FastMCP("Citation Counter")


@mcp.tool()
async def search_key_words(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for articles on Google Scholar using key words.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)

    Returns:
        List of dictionaries containing article information
    """
    try:
        results = await asyncio.to_thread(search, query, num_results)
        return results
    except Exception as e:
        return [{"error": f"An error occurred while searching Google Scholar: {str(e)}"}]