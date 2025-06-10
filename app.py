import gradio as gr  
from main import run_search_and_summarization  # Importing the function

def agentic_ai_interface(query, num_results=5, verbose=True):
    """Interface function to run the search & summarization."""
    return run_search_and_summarization(query, num_results, verbose)

# Gradio UI
iface = gr.Interface(
    fn=agentic_ai_interface,
    inputs=[
        gr.Textbox(label="Enter your query", placeholder="e.g., What is the latest research on quantum computing?"),
        gr.Slider(1, 10, value=5, label="Number of search results"),
    ],
    outputs="markdown",
    title="🔗 Agentic AI: Web Search + Summarizer",
    description="A multi-agent AI system that searches the web using DuckDuckGo and summarizes the results using a lightweight LLM."
)

if __name__ == "__main__":
    iface.launch()
