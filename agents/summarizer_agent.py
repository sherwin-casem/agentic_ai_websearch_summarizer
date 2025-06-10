from tools.summarizer_tool import summarize_text

def summarizer_agent(text):
    """
    Agent that summarizes the provided text using the summarization tool.

    Args:
        text (str): The text to summarize.

    Returns:
        str: The summarized version of the input text.
    """
    summary = summarize_text(text)
    return summary