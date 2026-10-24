
import streamlit as st


def display_dashboard_header():
    """
    Display the main dashboard heading.
    """

    st.title("AI Resume Intelligence")

    st.caption(
        "Understand your skills. Identify gaps. "
        "Build your career roadmap."
    )

    st.divider()


def display_overview_metrics(
    detected_skills,
    keyword_score,
    context_score
):
    """
    Display three core analysis metrics.
    """

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Detected Skills",
            detected_skills
        )

    with col2:
        st.metric(
            "Keyword Coverage",
            (
                f"{keyword_score:.1f}%"
                if keyword_score is not None
                else "N/A"
            )
        )

    with col3:
        st.metric(
            "Context-Aware Coverage",
            (
                f"{context_score:.1f}%"
                if context_score is not None
                else "N/A"
            )
        )

    st.caption(
        "Coverage is based on skill mentions and "
        "rule-based context classification. "
        "These scores do not measure verified "
        "proficiency or hiring probability."
    )


def create_dashboard_tabs():
    """
    Create the main navigation sections.
    """

    return st.tabs([
        "Overview",
        "Skill Analysis",
        "Learning Roadmap",
        "AI Insights",
        "Report"
    ])


def display_skill_badges(skills, status="info"):
    """
    Display a list of skills using Streamlit
    status components.
    """

    if not skills:
        st.info("No skills detected.")
        return

    for skill in skills:

        if status == "success":
            st.success(skill)

        elif status == "warning":
            st.warning(skill)

        elif status == "error":
            st.error(skill)

        else:
            st.info(skill)
