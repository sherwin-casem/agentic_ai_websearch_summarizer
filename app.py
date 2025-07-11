# app.py

import streamlit as st
from chains.langgraph_chains import (
    streamable_search,
    streamable_summarize_one,
    streamable_synthesize_final,
)
import json
from datetime import datetime

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="🔗 Agentic AI: Web Summarizer",
    layout="wide",  # Use wide layout for better information display
)

# --- UI Background Styling (no changes) ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/soham-x/assets/main/agentic_ai_bg.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.main > div {
    background: linear-gradient(180deg, #0f0f0fcc, #2e2e2ecc);
    border-radius: 15px;
    padding: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --- Title + Subtitle ---
st.markdown("<h1 style='text-align:center; color:#f1f1f1;'>🔍 Agentic AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#cccccc;'>Streaming Web Summarizer ✨</h3>", unsafe_allow_html=True)

# --- Session State Initialization ---
if "query_history" not in st.session_state:
    st.session_state.query_history = []
if "summaries" not in st.session_state:
    st.session_state.summaries = []
if "global_summary" not in st.session_state:
    st.session_state.global_summary = ""

# --- Input Form ---
with st.form("input_form"):
    query = st.text_input("💬 Enter your query:", placeholder="What is the latest research on quantum computing?")
    num_results = st.slider("📄 Number of search results", min_value=3, max_value=10, value=5)
    summarize_button = st.form_submit_button("🚀 Summarize Now")

# --- Main Logic ---
if summarize_button:
    if not query.strip():
        st.warning("⚠️ Please enter a query to begin.")
    else:
        # Reset state for a new query
        st.session_state.summaries = []
        st.session_state.global_summary = ""

        # --- 1. INSTANTLY SEARCH and show placeholders ---
        status_box = st.info("🔍 Performing web search...")
        search_results = streamable_search(query, num_results=num_results)
        
        if not search_results:
            status_box.error("❌ No relevant results found.")
        else:
            status_box.success(f"✅ Found {len(search_results)} sources. Now summarizing one by one...")
            
            # Create placeholders for each summary
            placeholders = [st.empty() for _ in search_results]
            
            # --- 2. STREAM SUMMARIES one by one ---
            for i, result in enumerate(search_results):
                placeholders[i].info(f"🧠 Summarizing: **{result.get('title', 'Source ' + str(i+1))}**...")
                
                summary_data = streamable_summarize_one(result)
                st.session_state.summaries.append(summary_data)
                
                # Update the placeholder with the actual summary content
                with placeholders[i].container():
                    st.markdown(f"**{i+1}. {summary_data['title']}**", unsafe_allow_html=True)
                    st.markdown(f"📝 {summary_data['summary']}", unsafe_allow_html=True)
                    st.markdown(f"🔗 [View Source]({summary_data['source']})", unsafe_allow_html=True)
                    with st.expander("🧠 Agent Thought Process"):
                        st.code(summary_data["thinking"])
                    st.markdown("---")

            # --- 3. SYNTHESIZE FINAL SUMMARY last ---
            status_box.info("🧠 Synthesizing a unified insight...")
            final_summary = streamable_synthesize_final(st.session_state.summaries)
            st.session_state.global_summary = final_summary
            status_box.empty() # Remove the status box

# --- Display Final Results ---
if st.session_state.global_summary:
    st.subheader("🧠 Unified Insight")
    st.markdown(f"📋 {st.session_state.global_summary}", unsafe_allow_html=True)
    st.markdown("---")

if st.session_state.summaries:
    st.subheader("Individual Summaries")
    # This part is now handled by the placeholders above, but you could re-display if needed
    st.success("All summaries generated.")
