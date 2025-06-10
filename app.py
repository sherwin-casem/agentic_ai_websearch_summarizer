import gradio as gr
from chains.langgraph_chain import run_chain

def agentic_ai_interface(query, verbose=True):
    """
    Interface function to run the agentic AI chain.

    Args:
        query (str): User's input query.
        verbose (bool): Whether to show detailed reasoning.

    Returns:
        str or dict: Final summary or verbose output.
    """
    result = run_chain(query, verbose=verbose)
    if verbose:
        return f"🔍 **Search Results:**\n\n" + \
               "\n".join([f"- {r.get('title', 'No Title')} ({r.get('href', 'No URL')})" for r in result['search_results']]) + \
               f"\n\n📝 **Summary:**\n\n{result['summary']}"
    else:
        return result

# Gradio UI
iface = gr.Interface(
    fn=agentic_ai_interface,
    inputs=[
        gr.Textbox(label="Enter your query", placeholder="e.g., What is the latest research on quantum computing?"),
        gr.Checkbox(label="Verbose Output", value=True)
    ],
    outputs="markdown",
    title="🔗 Agentic AI: Web Search + Summarizer",
    description="A multi-agent AI system that searches the web using DuckDuckGo and summarizes the results using a lightweight LLM."
)

if __name__ == "__main__":
    iface.launch()