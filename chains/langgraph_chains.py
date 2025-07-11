# chains/langgraph_chains.py

from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from typing import Dict, Any, List

def streamable_search(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Performs the web search and returns the results. This is a fast operation.
    """
    search_results = search_agent(query, num_results=num_results)
    return search_results

def streamable_summarize_one(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarizes a single search result. This is the slow part (LLM call).
    """
    title = result.get("title", "No Title")
    source = result.get("href", "")
    content = result.get("body", "") or result.get("text", "")
    token_count = len(content.split())

    summary = summarizer_agent(
        body=content,
        source=source,
        title=title,
    )

    # Create the "thinking" log for the expander
    thought_log = (
        f"🤔 Agent reads: {title}\n"
        f"📚 Extracting claims from content.\n"
        f"🔤 Tokens: {token_count}"
    )

    return {
        "title": title,
        "source": source,
        "summary": summary,
        "thinking": thought_log,
    }

def streamable_synthesize_final(summaries: List[Dict[str, Any]]) -> str:
    """
    Takes a list of individual summaries and creates a final, unified insight.
    """
    if not summaries:
        return "No individual summaries were generated to synthesize."

    combined_text = "\n\n".join(s["summary"] for s in summaries)
    
    # Using the same prompt format as before for consistency
    synthesis_prompt = (
        "<|im_start|>system\n"
        "You are a scholarly assistant synthesizing multiple independent web summaries.<|im_end|>\n"
        "<|im_start|>user\n"
        "Combine the following insights into a unified high-level overview:\n\n"
        f"{combined_text}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    final_summary = summarizer_agent(synthesis_prompt)
    return final_summary
