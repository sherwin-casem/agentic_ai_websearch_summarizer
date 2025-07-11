# agents/search_agent.py

# FIX: Importing from the canonical tools file, not the conflicting chromadb file.
from tools.duckduckgo_tools import search_duckduckgo
from typing import List, Dict, Any

def search_agent(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Agent wrapper around the cached DuckDuckGo search.
    """
    # FIX: Using the correct keyword 'num_results' to match the function definition.
    results = search_duckduckgo(query, num_results=num_results)

    for r in results:
        r["text"] = r.get("body", "") or r.get("snippet", "")  # Normalize for Chroma
    return results
