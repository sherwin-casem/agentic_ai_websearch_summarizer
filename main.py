from duckduckgosearch_tool import search_duckduckgo  
from summarizer_tool import summarize_text  

def run_search_and_summarization(query: str, num_results: int = 5, verbose: bool = True):
    """Performs a DuckDuckGo web search and summarizes results."""
    
    print(f"\n🔍 Searching DuckDuckGo for: {query}\n")

    # Step 1: Perform Web Search
    search_results = search_duckduckgo(query, num_results)

    if not search_results:
        return "❌ No relevant results found. Try another query."

    # Step 2: Summarize Each Search Result
    result_text = "\n📌 **Summarized Results:**\n\n"
    for idx, result in enumerate(search_results, start=1):
        summary = summarize_text(result.get("body", "No content available"))
        result_text += f"{idx}. **{result.get('title', 'No Title')}**\n   {summary}\n\n"

    return result_text.strip()  # Ensuring clean output formatting

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DuckDuckGo Web Search + AI Summarization")
    parser.add_argument("query", type=str, help="Enter your search query")
    parser.add_argument("--num_results", type=int, default=5, help="Number of search results to fetch")
    args = parser.parse_args()

    print(run_search_and_summarization(args.query, args.num_results))