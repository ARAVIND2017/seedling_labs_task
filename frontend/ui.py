import streamlit as st
import requests
import json

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="GitHub Issue AI Assistant",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------
# Session State
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "result" not in st.session_state:
    st.session_state.result = None


# -------------------------------
# Common Styles
# -------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 10px;
}
.subtitle {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 30px;
}
.card {
    padding: 25px;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
}
.label {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# PAGE 1 : HOME
# -------------------------------
if st.session_state.page == "home":
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("<div class='main-title'>AI Powered GitHub Issue Assistant</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='subtitle'>Analyze GitHub issues instantly using AI. "
            "Get structured insights, priority scoring, and actionable labels in seconds.</div>",
            unsafe_allow_html=True
        )

        st.markdown("✔️ Fast analysis  \n✔️ Clean structured output  \n✔️ Developer friendly")

        if st.button("🚀 Get Started"):
            st.session_state.page = "form"
            st.rerun()

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=900",
            use_container_width=True
        )


# -------------------------------
# PAGE 2 : FORM
# -------------------------------
elif st.session_state.page == "form":
    st.markdown("<div class='main-title'>Analyze a GitHub Issue</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Enter the repository URL and issue number below.</div>", unsafe_allow_html=True)

    form_col1, form_col2, form_col3 = st.columns([1, 2, 1])

    with form_col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        github_repo = st.text_input("GitHub Repository URL", placeholder="https://github.com/facebook/react")
        issue_number = st.text_input("Issue Number", placeholder="e.g. 123")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            analyze_clicked = st.button("🔍 Analyze Issue")

        with col_btn2:
            back_clicked = st.button("⬅️ Back")

        st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked:
        if not github_repo or not issue_number:
            st.error("Please provide both repository URL and issue number.")
        else:
            with st.spinner("Analyzing issue with AI..."):
                try:
                    payload = {
                        "repo_url": github_repo,
                        "issue_number": int(issue_number)
                    }

                    response = requests.post(
                        "http://127.0.0.1:8000/analyze-issue",
                        json=payload,
                        timeout=120
                    )

                    # ✅ Friendly Error Handling Added
                    if response.status_code == 200:
                        st.session_state.result = response.json()
                        st.session_state.page = "result"
                        st.rerun()

                    elif response.status_code == 404:
                        st.warning("❌ Issue number not found in this repository. Please verify the issue number and try again.")

                    else:
                        st.error("⚠️ Something went wrong while processing your request. Please try again later.")

                except Exception as error:
                    st.error(f"Request failed: {error}")

    if back_clicked:
        st.session_state.page = "home"
        st.rerun()


# -------------------------------
# PAGE 3 : RESULT
# -------------------------------
elif st.session_state.page == "result":
    st.markdown("<div class='main-title'>Analysis Result</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>AI generated structured insights for the selected GitHub issue.</div>", unsafe_allow_html=True)

    result = st.session_state.result
    analysis_text = result.get("analysis", "")

    # Parse JSON
    parsed_analysis = {}
    try:
        parsed_analysis = json.loads(analysis_text)
    except Exception:
        st.warning("AI response could not be parsed as structured JSON.")

    tab1, tab2 = st.tabs(["📖 Summary View", "🧾 JSON View"])

    # -------- Summary View --------
    with tab1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if parsed_analysis:
            st.markdown("### 📝 Summary")
            st.info(parsed_analysis.get("summary", "N/A"))

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Type:** {parsed_analysis.get('type', 'N/A')}")
                st.markdown(f"**Priority:** {parsed_analysis.get('priority_score', 'N/A')}")

            with col2:
                st.markdown(f"**Potential Impact:** {parsed_analysis.get('potential_impact', 'N/A')}")

            st.markdown("### 🏷️ Suggested Labels")
            labels = parsed_analysis.get("suggested_labels", [])
            if labels:
                for label in labels:
                    st.success(label)
            else:
                st.write("No labels generated.")
        else:
            st.write("No structured data available.")

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- JSON View --------
    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.code(result.get("analysis", ""), language="json")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    col_nav1, col_nav2 = st.columns([1, 1])

    with col_nav1:
        if st.button("🔄 Analyze Another"):
            st.session_state.page = "form"
            st.rerun()

    with col_nav2:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            st.rerun()
