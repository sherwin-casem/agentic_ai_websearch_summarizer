from duckduckgo_search import DDGS
from typing import List, Dict

def search_duckduckgo(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Performs a web search using the DuckDuckGo API and returns the results.

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        List[Dict[str, str]]: A list of search results, each containing
                               a title, URL (href), and snippet (body).
    """
    print(f"Searching for '{query}'...")
    with DDGS() as ddgs:
        # Using ddgs.text() which is a generator
        results = [r for r in ddgs.text(query, max_results=num_results)]
    print(f"Found {len(results)} results.")
    return results

# Example usage:
if __name__ == '__main__':
    search_results = search_duckduckgo("What is agentic AI?", num_results=3)
    if search_results:
        for result in search_results:
            print(f"Title: {result['title']}")
            print(f"URL: {result['href']}")
            print(f"Snippet: {result['body']}")
            print("-" * 20)
