🧠 System Architecture Overview
🔹 Agents and Tools
Search Agent

Tool: DuckDuckGo Search API (via duckduckgo_search Python package or custom wrapper)
Function: Searches the web for relevant pages based on user query.
Summarization Agent

Tool: Text summarization using a lightweight LLM
Function: Summarizes the content retrieved by the Search Agent.
🧩 Tech Stack
1. LLM (Brain of the Agent)
Model: Phi-2 or TinyLlama-1.1B
Why: Both are ~1B parameter models, fast on a single T4 GPU, and support instruct tuning.
Runner: transformers + accelerate or vLLM for optimized inference.
2. Vector DB
Choice: ChromaDB (lightweight, open-source, and easy to integrate)
Use: Store and retrieve embeddings for context-aware summarization.
3. LangChain Ecosystem
Core Framework: LangGraph (for multi-agent workflows)
Agent Logic: ReAct (Reason + Act) with verbose logging
Tool Integration: DuckDuckGo + Summarizer as LangChain tools
4. Frontend
Framework: Streamlit (lightweight, Lightning AI Studio compatible)
UI: Simple input box for query, output box for verbose reasoning and final summary
🔧 Implementation Plan
✅ Step 1: Define Tools
DuckDuckGo Tool: Use duckduckgo_search to fetch top 5 URLs and snippets.
Summarizer Tool: Use the selected LLM to summarize combined snippets.
✅ Step 2: Build Agents
Search Agent: Calls DuckDuckGo tool, returns results.
Summarizer Agent: Takes results, summarizes using LLM.
✅ Step 3: LangGraph Workflow
Define nodes:
InputNode → SearchAgent → SummarizerAgent → OutputNode
Use ReAct-style prompts for reasoning steps.
✅ Step 4: Streamlit UI
Input: User query
Output: Verbose reasoning + final summary
🧪 Performance Tips
Use sentence-transformers/all-MiniLM-L6-v2 for fast embedding generation.
Cache DuckDuckGo results to reduce latency.
Use LangSmith for debugging and tracing agent steps.
🚀 Deployment on Lightning AI Studio
Lightning supports Streamlit apps and HuggingFace models.
Use lightning_app to wrap the Streamlit interface.
Ensure all dependencies are in requirements.txt.

📦 Installation steps (locally):
1. Cretae a python virtual environment variable
   python -m venv env
2. Activate the env
   .\env\scripts\activate
3. Install the dependencies
   pip install -r requirements.txt
4. Run the app.py file
   streamlit run app.py

Or else view the deployed version from here: 
