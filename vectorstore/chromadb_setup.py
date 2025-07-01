# tools/chroma_db.py

from duckduckgo_search import DDGS
from typing import List, Dict, Any

def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a DuckDuckGo search and return the results.
    """
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=max_results)]
    return results
