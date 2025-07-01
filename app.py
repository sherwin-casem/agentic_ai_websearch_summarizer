import streamlit as st
from chains.langgraph_chains import run_chain
import json
from datetime import datetime

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="🔗 Agentic AI: Web Summarizer",
    layout="centered",
)

# --- UI Background Styling ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://raw.githubusercontent.com/soham-x/assets/main/agentic_ai_bg.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
section.main > div {
    background: linear-gradient(180deg, #0f0f0fcc, #2e2e2ecc);
    border-radius: 15px;
    padding: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --- Title + Subtitle ---
st.markdown("<h1 style='text-align:center; color:#f1f1f1;'>🔍 Agentic AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#cccccc;'>Web Search + Summarizer Powered by LLMs ✨</h3>", unsafe_allow_html=True)

# --- Session Memory ---

if "query_history" not in st.session_state:
    st.session_state.query_history = []

# --- Input ---
query = st.text_input("💬 Enter your query:", placeholder="What is the latest research on quantum computing?")
num_results = st.slider("📄 Number of search results", min_value=1, max_value=10, value=5)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Summarize", "📊 Feedback Log", "📚 History"])

# --- Summarization Tab ---
with tab1:
    if st.button("🚀 Summarize Now", key="summarize_button"):
        if not query.strip():
            st.warning("⚠️ Please enter a query to begin.")
        else:
            status_box = st.empty()

            def status_callback(msg: str) -> None:
                status_box.info(msg)

            with st.spinner("⏳ Summarizing..."):
                try:
                    result = run_chain(query, verbose=True, status_callback=status_callback)
                except Exception as e:
                    st.error(f"🚫 Chain execution error: {e}")
                    result = None

            status_box.empty()

            if not result:
                st.error("❌ No relevant results found.")
            else:
                st.success("📌 Summarized Results")
                st.session_state.query_history.append({"query": query, "result": result}) # type: ignore

                if "global_summary" in result and result["global_summary"]:
                    st.subheader("🧠 Unified Insight")
                    st.markdown(f"📋 {result['global_summary']}", unsafe_allow_html=True)
                    st.markdown("---")

                for i, s in enumerate(result.get("results", [])):
                    st.markdown(f"**{i+1}. {s['title']}**", unsafe_allow_html=True)
                    st.markdown(f"📝 {s['summary']}", unsafe_allow_html=True)
                    st.markdown(f"🔗 [View Source]({s['source']})", unsafe_allow_html=True)

                    with st.expander("🧠 Agent Thought Process"):
                        st.code(s["thinking"])

                    feedback = st.radio(
                        f"🎯 Was this summary accurate?",
                        ["👍 Yes", "👎 No"],
                        key=f"feedback_{i}",
                        horizontal=True
                    )

                    if feedback == "👎 No":
                        user_edit = st.text_area("✍️ Suggest an improvement:", key=f"edit_{i}")
                        if user_edit.strip():
                            feedback_data: dict[str, str] = {
                                "query": query,
                                "source": s["source"],
                                "title": s["title"],
                                "old_summary": s["summary"],
                                "user_edit": user_edit,
                                "timestamp": datetime.now().isoformat()
                            }
                            with open("feedback_log.jsonl", "a") as f:
                                f.write(json.dumps(feedback_data) + "\n")

                    st.markdown("---")

# --- Feedback Log Tab ---
with tab2:
    try:
        with open("feedback_log.jsonl", "r") as f:
            entries = [json.loads(line) for line in f.readlines()]
        st.info(f"📈 Total feedback entries: {len(entries)}")
        for i, entry in enumerate(reversed(entries), start=1):
            st.markdown(f"**{i}. {entry['title']}**")
            st.markdown(f"🔗 [Source]({entry['source']})")
            st.markdown(f"📝 Original Summary:\n> {entry['old_summary']}")
            st.markdown(f"✍️ Suggested Edit:\n> {entry['user_edit']}")
            st.markdown(f"🕒 {entry['timestamp']}")
            st.markdown("---")
    except FileNotFoundError:
        st.warning("No feedback has been submitted yet.")

# --- History Tab ---
with tab3:
    if st.session_state.query_history: # type: ignore
        for i, q in enumerate(reversed(st.session_state.query_history), start=1): # type: ignore
            st.markdown(f"**{i}.** _{q['query']}_")
            st.markdown(f"🧠 Unified Insight: {q['result'].get('global_summary', 'N/A')}") # type: ignore
            st.markdown("---")
    else:
        st.info("No prior summarization history in this session.")
