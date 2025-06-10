from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent

def run_chain(query, verbose=True):
    """
    Executes the multi-agent chain: search → summarize.

    Args:
        query (str): The user's input query.
        verbose (bool): If True, returns detailed reasoning steps.

    Returns:
        dict or str: Final summary or verbose output with reasoning steps.
    """
    if verbose:
        print("🔍 Step 1: Performing web search...")
    search_results = search_agent(query)

    if verbose:
        print(f"✅ Retrieved {len(search_results)} results.")
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result.get('title', 'No Title')} - {result.get('href', 'No URL')}")

    combined_text = " ".join([result.get("body", result.get("text", "")) for result in search_results])

    if verbose:
        print("\n📝 Step 2: Summarizing the combined search results...")

    summary = summarizer_agent(combined_text)

    if verbose:
        return {
            "query": query,
            "search_results": search_results,
            "combined_text": combined_text[:1000] + "...",  # Truncate for readability
            "summary": summary
        }
    else:
        return summary
