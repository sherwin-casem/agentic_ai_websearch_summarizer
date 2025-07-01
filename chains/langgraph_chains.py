from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from typing import Optional, Callable, Dict, Any, List

def run_chain(
    query: str,
    verbose: bool = True,
    status_callback: Optional[Callable[[str], None]] = None,
    persist_id: Optional[str] = None
) -> Dict[str, Any]:
    if verbose and status_callback:
        status_callback("🔍 Step 1: Performing web search...")

    search_results = search_agent(query)

    if not search_results:
        return {
            "global_summary": "",
            "results": []
        }

    summaries: List[Dict[str, Any]] = []

    for i, result in enumerate(search_results):
        title = result.get("title", f"Source {i+1}")
        source = result.get("href", "")
        content = result.get("body", "") or result.get("text", "")

        token_count = len(content.split())
        thought_log = (
            f"🤔 Agent reads: {title}\n"
            f"📚 Extracting claims from content.\n"
            f"🔤 Tokens: {token_count}"
        )

        if verbose and status_callback:
            status_callback(f"🧠 Analyzing **{title}**...\n🧾 `{token_count}` tokens")

        summary = summarizer_agent(
            body=content,
            source=source,
            title=title,
        )

        summaries.append({
            "title": title,
            "source": source,
            "summary": summary,
            "thinking": thought_log,
        })

    combined_text = "\n\n".join(s["summary"] for s in summaries)
    synthesis_prompt = (
        "<|system|>\nYou are a scholarly assistant synthesizing multiple independent web summaries.\n"
        "<|user|>\nCombine the following insights into a unified high-level overview:\n\n"
        f"{combined_text}<|assistant|>\n"
    )

    if verbose and status_callback:
        status_callback("🧠 Synthesizing a unified insight...")

    final_summary = summarizer_agent(synthesis_prompt)

    return {
        "global_summary": final_summary,
        "results": summaries
    }
