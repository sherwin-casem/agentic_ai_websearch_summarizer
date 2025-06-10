import gradio as gr
from tools.duckduckgo_tools import search_duckduckgo  # Updated import path
from tools.summarizer_tool import summarize_text  # Updated import path

def agentic_ai_interface(query, num_results=5, verbose=True):
    """Interface function to run the search & summarization."""
    
    search_results = search_duckduckgo(query, max_results=num_results)

    if not search_results:
        return "❌ No relevant results found. Try another query."

    # Generate summaries
    result_text = "\n📌 **Summarized Results:**\n\n"
    for idx, result in enumerate(search_results, start=1):
        summary = summarize_text(result.get("body", "No content available"))
        result_text += f"{idx}. **{result.get('title', 'No Title')}**\n   {summary}\n\n"

    return result_text.strip()

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
    iface.launch(share=True)
