from tools.duckduckgo_tool import search_duckduckgo

def search_agent(query):
    """
    Agent that uses the DuckDuckGo tool to perform a web search.

    Args:
        query (str): The user's search query.

    Returns:
        list: A list of search result dictionaries.
    """
    results = search_duckduckgo(query)
    return results
