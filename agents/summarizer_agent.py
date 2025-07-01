from tools.summarizer_tool import summarize_text

def summarizer_agent(
    body: str,
    source: str = "",
    title: str = ""
) -> str:
    """
    Agent that summarizes a text and appends source metadata.

    Args:
        body (str): The main content to summarize.
        source (str): Source URL or reference.
        title (str): Document or webpage title.

    Returns:
        str: Summary with source attribution.
    """
    summary = summarize_text(body)
    source_line = f"\n🔗 Source: [{title or 'View Original'}]({source})" if source else ""
    return f"{summary}{source_line}"
