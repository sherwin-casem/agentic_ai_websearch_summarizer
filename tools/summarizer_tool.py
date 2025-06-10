from transformers import pipeline

def summarize_text(text, model_name="facebook/bart-large-cnn"):
    """
    Summarize the given text using a transformer-based summarization model.

    Args:
        text (str): The text to summarize.
        model_name (str): The name of the model to use for summarization.

    Returns:
        str: The summarized text.
    """
    summarizer = pipeline("summarization", model=model_name)
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']