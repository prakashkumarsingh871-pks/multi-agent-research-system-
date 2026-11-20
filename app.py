import re
from datetime import datetime
import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Minimal CSS: clean spacing and neutral borders, no glow or decorative effects
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1080px;
        }
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 6px;
            padding: 0.75rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def extract_score(feedback: str) -> str:
    match = re.search(r"Score\s*:\s*([0-9]+(?:\.[0-9]+)?\s*/\s*10)", feedback, re.IGNORECASE)
    return match.group(1).replace(" ", "") if match else "N/A"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return slug[:60] or "research_report"


if "history" not in st.session_state:
    st.session_state.history = []

if "active_result" not in st.session_state:
    st.session_state.active_result = None


# Sidebar: pipeline stages and session history
with st.sidebar:
    st.header("Pipeline Stages")
    st.markdown(
        """
        1. **Search Agent** - Queries the web via Tavily
        2. **Reader Agent** - Scrapes the most relevant source
        3. **Writer Chain** - Drafts a structured report
        4. **Critic Chain** - Reviews and scores the report
        """
    )

    st.divider()
    st.header("Recent Runs")

    if not st.session_state.history:
        st.caption("No research runs yet.")
    else:
        for idx, item in enumerate(st.session_state.history):
            label = f"{item['topic']} ({item['timestamp']})"
            if st.button(label, key=f"history_{idx}", width="stretch"):
                st.session_state.active_result = item

        st.write("")
        if st.button("Clear History", width="stretch"):
            st.session_state.history = []
            st.session_state.active_result = None
            st.rerun()


# Main Header
st.title("Multi-Agent Research System")
st.caption("Enter a topic to run web search, source scraping, report drafting, and critical review.")

# Topic input form
with st.form("research_form", clear_on_submit=False):
    col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
    with col_input:
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g., Current advances in solid-state batteries",
        )
    with col_btn:
        submitted = st.form_submit_button("Run", type="primary", width="stretch")

if submitted:
    clean_topic = topic.strip()
    if not clean_topic:
        st.warning("Please enter a research topic.")
    else:
        progress_bar = st.progress(0, text="Starting pipeline...")
        status_box = st.status("Running research pipeline...", expanded=True)

        def on_step(step: int, message: str) -> None:
            progress_map = {1: 15, 2: 40, 3: 65, 4: 85, 5: 100}
            progress_bar.progress(progress_map.get(step, 0), text=message)
            status_box.write(message)

        try:
            state = run_research_pipeline(clean_topic, on_step=on_step)
            status_box.update(label="Research completed", state="complete", expanded=False)

            record = {
                "topic": clean_topic,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "state": state,
            }
            st.session_state.history.insert(0, record)
            st.session_state.active_result = record
        except Exception as exc:
            status_box.update(label="Pipeline failed", state="error", expanded=True)
            st.error(f"Error while running pipeline: {exc}")


# Render active results
active = st.session_state.active_result
if active:
    state = active["state"]
    report_text = state.get("report", "")
    feedback_text = state.get("feedback", "")
    search_text = state.get("search_results", "")
    scraped_text = state.get("scraped_content", "")

    st.divider()
    header_col, action_col = st.columns([4, 1], vertical_alignment="center")
    with header_col:
        st.subheader(active["topic"])
        st.caption(f"Completed at {active['timestamp']}")
    with action_col:
        st.download_button(
            label="Download Report (.md)",
            data=report_text,
            file_name=f"{slugify(active['topic'])}.md",
            mime="text/markdown",
            width="stretch",
        )

    tab_report, tab_critic, tab_search, tab_scraped = st.tabs(
        ["Report", "Critic Review", "Search Results", "Scraped Content"]
    )

    with tab_report:
        st.markdown(report_text)

    with tab_critic:
        score = extract_score(feedback_text)
        metric_col, _ = st.columns([1, 3])
        with metric_col:
            st.metric(label="Critic Score", value=score)
        st.markdown(feedback_text)

    with tab_search:
        st.markdown(search_text)

    with tab_scraped:
        st.markdown(scraped_text)
