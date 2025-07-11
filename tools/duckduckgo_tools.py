# tools/duckduckgo_tools.py

# FIX: Using the new, recommended 'ddgs' library instead of the deprecated 'duckduckgo_search'
from ddgs import DDGS
from typing import List, Dict
from functools import lru_cache

@lru_cache(maxsize=128)
def search_duckduckgo(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Performs a web search using the DDGS API and returns the results.
    """
    print(f"Searching for '{query}' with {num_results} results...")
    # The DDGS object usage remains the same, which makes for an easy upgrade.
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=num_results)]
    print(f"Found {len(results)} results.")
    return results

# Example usage:
if __name__ == '__main__':
    search_results = search_duckduckgo("What is agentic AI?", num_results=3)
    if search_results:
        for r in search_results:
            print(r)
