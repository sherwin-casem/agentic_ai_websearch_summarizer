# agents/search_agent.py

from vectorstore.chromadb_setup import search_duckduckgo
from typing import List, Dict, Any

def search_agent(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Agent wrapper around DuckDuckGo search.
    """
    results = search_duckduckgo(query, max_results=num_results)

    for r in results:
        r["text"] = r.get("body", "") or r.get("snippet", "")  # Normalize for Chroma
    return results
