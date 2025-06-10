from duckduckgo_search import ddg

def search_duckduckgo(query, max_results=5):
    """
    Perform a DuckDuckGo search and return the results.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return.

    Returns:
        list: A list of dictionaries containing the search results.
    """
    results = ddg(query, max_results=max_results)
    return results
