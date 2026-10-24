
import streamlit as st
import plotly.graph_objects as go

from components.dashboard import (
    display_dashboard_header,
    display_overview_metrics,
    create_dashboard_tabs,
    display_skill_badges
)

from utils.skill_extractor import load_skills
from utils.skill_gap_analyzer import analyze_skill_gap
from utils.intelligence_engine import generate_intelligence_results
from utils.semantic_matcher import find_semantic_matches
from utils.report_generator import generate_pdf_report
from utils.visualizer import (
    create_skill_coverage_chart,
    create_priority_chart
)
from utils.input_validator import (
    InputValidationError,
    validate_resume,
    validate_job_description
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

display_dashboard_header()


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def create_context_category_chart(analysis):
    """Create category chart using context-aware results."""

    database = load_skills()

    matched = set(analysis["matched_skills"])
    missing = set(analysis["missing_skills"])
    job_skills = set(analysis["job_skills"])

    categories = []
    matched_counts = []
    missing_counts = []

    for category, skills in database.items():

        relevant = set(skills.keys()) & job_skills

        if not relevant:
            continue

        categories.append(category)
        matched_counts.append(len(relevant & matched))
        missing_counts.append(len(relevant & missing))

    if not categories:
        return None

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            name="Matched",
            x=categories,
            y=matched_counts,
            marker_color="#16a34a"
        )
    )

    figure.add_trace(
        go.Bar(
            name="Not Evidenced",
            x=categories,
            y=missing_counts,
            marker_color="#ef4444"
        )
    )

    figure.update_layout(
        title="Context-Aware Skills by Category",
        barmode="group",
        xaxis_title="Skill Category",
        yaxis_title="Number of Skills",
        yaxis=dict(dtick=1)
    )

    return figure


def run_analysis(resume_file, job_text):
    """Validate inputs and run all intelligence engines."""

    cleaned_job = validate_job_description(job_text)

    with st.spinner("Reading and validating resume..."):
        resume_text = validate_resume(resume_file)

    with st.spinner("Analyzing technical skills..."):
        intelligence = generate_intelligence_results(
            resume_text,
            cleaned_job
        )

        keyword_analysis = analyze_skill_gap(
            resume_text,
            cleaned_job
        )

    with st.spinner("Running AI semantic matching..."):
        semantic_results = find_semantic_matches(
            resume_text,
            cleaned_job
        )

    return {
        "resume_text": resume_text,
        "job_description": cleaned_job,
        "intelligence": intelligence,
        "keyword_analysis": keyword_analysis,
        "semantic_results": semantic_results
    }


def show_skills(title, skills, status="info"):
    """Display a titled group of skills."""

    st.markdown(f"**{title}**")

    if skills:
        display_skill_badges(skills, status)
    else:
        st.caption("None detected.")


# ==========================================
# 3. INPUT SECTION
# ==========================================

st.subheader("Start Your Analysis")

input_col1, input_col2 = st.columns(2)

with input_col1:

    resume = st.file_uploader(
        "Upload Your Resume",
        type=["pdf", "docx"],
        help="Upload a PDF or DOCX resume, maximum 5 MB."
    )

with input_col2:

    job_description = st.text_area(
        "Job Description",
        height=180,
        placeholder=(
            "Paste the role description, required skills, "
            "and preferred qualifications..."
        )
    )

st.caption(
    "Supported formats: PDF and DOCX | "
    "Maximum size: 5 MB"
)


# ==========================================
# 4. ANALYZE BUTTON
# ==========================================

if st.button(
    "Analyze Resume",
    type="primary"
):

    # Clear old analysis and PDF state
    for key in ["results", "pdf_bytes", "pdf_error"]:
        st.session_state.pop(key, None)

    try:

        st.session_state["results"] = run_analysis(
            resume,
            job_description
        )

        st.success("Resume analysis completed!")

    except InputValidationError as error:

        st.warning(str(error))

    except Exception as error:

        st.error(
            "An unexpected error occurred during analysis."
        )

        # For local development only
        with st.expander("Technical Error Details"):
            st.exception(error)


# ==========================================
# 5. RESULTS DASHBOARD
# ==========================================

if "results" in st.session_state:

    results = st.session_state["results"]

    resume_text = results["resume_text"]
    intelligence = results["intelligence"]

    skills = intelligence["skills"]
    analysis = intelligence["analysis"]
    priorities = intelligence["priorities"]
    roadmap = intelligence["roadmap"]
    classified = intelligence["classified"]
    context_results = intelligence["context_results"]

    keyword_analysis = results["keyword_analysis"]
    semantic_results = results["semantic_results"]

    total_skills = sum(
        len(items)
        for items in skills.values()
    )

    keyword_score = keyword_analysis["match_score"]
    context_score = analysis["match_score"]

    st.divider()

    # ======================================
    # SUMMARY METRICS
    # ======================================

    display_overview_metrics(
        detected_skills=total_skills,
        keyword_score=keyword_score,
        context_score=context_score
    )

    st.divider()

    # ======================================
    # NAVIGATION TABS
    # ======================================

    (
        overview_tab,
        skills_tab,
        roadmap_tab,
        ai_tab,
        report_tab
    ) = create_dashboard_tabs()


    # ======================================
    # TAB 1: OVERVIEW
    # ======================================

    with overview_tab:

        st.header("Analysis Overview")

        matched_count = len(
            analysis["matched_skills"]
        )

        missing_count = len(
            analysis["missing_skills"]
        )

        high_count = sum(
            item["priority"] == "High"
            for item in priorities
        )

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "Matched Job Skills",
                matched_count
            )

        with b:
            st.metric(
                "Skills Requiring Attention",
                missing_count
            )

        with c:
            st.metric(
                "High-Priority Gaps",
                high_count
            )

        if context_score is not None:

            st.subheader("Context-Aware Coverage")

            st.progress(
                max(0.0, min(context_score / 100, 1.0))
            )

        st.caption(
            "Coverage measures detected resume evidence "
            "against recognized job skills. "
            "It is not an ATS score or verified proficiency."
        )

        st.subheader("Visual Analytics")

        coverage_fig = create_skill_coverage_chart(
            analysis
        )

        priority_fig = create_priority_chart(
            priorities
        )

        category_fig = create_context_category_chart(
            analysis
        )

        chart1, chart2 = st.columns(2)

        with chart1:

            if coverage_fig is not None:
                st.plotly_chart(
                    coverage_fig,
                    width="stretch"
                )
            else:
                st.info("No coverage chart available.")

        with chart2:

            if priority_fig is not None:
                st.plotly_chart(
                    priority_fig,
                    width="stretch"
                )
            else:
                st.info("No priority chart available.")

        if category_fig is not None:

            st.plotly_chart(
                category_fig,
                width="stretch"
            )

        else:

            st.info("No category comparison available.")


    # ======================================
    # TAB 2: SKILL ANALYSIS
    # ======================================

    with skills_tab:

        st.header("Detailed Skill Analysis")

        st.subheader("Detected Technical Skills")

        if skills:

            for category, items in skills.items():

                with st.expander(
                    f"{category} ({len(items)} skills)"
                ):
                    st.write(", ".join(items))

        else:
            st.info("No technical skills detected.")

        st.divider()

        st.subheader("Context-Aware Classification")

        resolved = context_results["resolved"]

        context_col1, context_col2 = st.columns(2)

        with context_col1:

            show_skills(
                "Demonstrated",
                resolved["demonstrated"],
                "success"
            )

            show_skills(
                "Currently Learning",
                resolved["learning"],
                "warning"
            )

            show_skills(
                "Interested",
                resolved["interested"]
            )

        with context_col2:

            show_skills(
                "Negated",
                resolved["negated"],
                "error"
            )

            show_skills(
                "Conflicting Evidence",
                resolved["conflicting"],
                "warning"
            )

        st.caption(
            "Context classifications are inferred from "
            "resume language, not independently verified."
        )

        st.divider()

        st.subheader("Job Skill Matching")

        matched_col, missing_col = st.columns(2)

        with matched_col:

            show_skills(
                "Matched Skills",
                analysis["matched_skills"],
                "success"
            )

        with missing_col:

            show_skills(
                "Skills Requiring Attention",
                analysis["missing_skills"],
                "error"
            )

        with st.expander("Detailed Skill Gap Breakdown"):

            for label, key in [
                ("Learning", "learning_skills"),
                ("Interested", "interested_skills"),
                ("Negated", "negated_skills"),
                ("Conflicting", "conflicting_skills"),
                ("Not Mentioned", "unmentioned_skills")
            ]:

                st.markdown(f"**{label}**")

                st.write(
                    ", ".join(analysis[key])
                    or "None"
                )

        st.divider()

        st.subheader("Skill Gap Priorities")

        if priorities:

            for item in priorities:

                st.markdown(
                    f"**{item['skill']}** — "
                    f"{item['priority']} Priority"
                )

                st.caption(
                    f"Resume context: {item['context']} | "
                    f"Job classification: {item['category']}"
                )

        else:
            st.success(
                "No recognized skill gaps requiring attention."
            )

        with st.expander("Job Requirement Classification"):

            for label, key in [
                ("Required", "required"),
                ("Preferred", "preferred"),
                ("Unclassified", "unclassified")
            ]:

                st.markdown(f"**{label}**")

                st.write(
                    ", ".join(classified[key])
                    or "None"
                )


    # ======================================
    # TAB 3: LEARNING ROADMAP
    # ======================================

    with roadmap_tab:

        st.header("Personalized Learning Roadmap")

        st.caption(
            "Recommendations reflect job priorities "
            "and the context of detected resume skills."
        )

        if roadmap:

            st.metric(
                "Recommended Learning Steps",
                len(roadmap)
            )

            for item in roadmap:

                heading = (
                    f"Step {item['step']} — "
                    f"{item['skill']} "
                    f"({item['priority']} Priority)"
                )

                with st.expander(heading):

                    st.markdown("**Current Status**")
                    st.info(item["status"])

                    st.markdown("**Recommended Action**")
                    st.write(item["action"])

                    st.markdown("**Personalized Guidance**")
                    st.write(item["guidance"])

                    st.markdown("**Topics to Learn**")

                    for index, topic in enumerate(
                        item["topics"]
                    ):

                        st.checkbox(
                            topic,
                            key=(
                                f"roadmap_{item['skill']}_{index}"
                            )
                        )

                    st.markdown("**Practice Project**")
                    st.success(item["project"])

                    st.markdown("**Learning Resource**")

                    if item["resource"]:

                        st.markdown(
                            f"[Open Learning Resource]"
                            f"({item['resource']})"
                        )

                    else:
                        st.caption(
                            "No curated resource available."
                        )

        else:

            st.success(
                "No learning gaps identified within "
                "our supported skill vocabulary."
            )


    # ======================================
    # TAB 4: AI INSIGHTS
    # ======================================

    with ai_tab:

        st.header("AI Semantic Insights")

        st.write(
            "The model identifies resume statements "
            "that are semantically related to job requirements."
        )

        st.caption(
            "A high similarity score does not verify "
            "experience or guarantee job suitability."
        )

        if semantic_results:

            st.metric(
                "Requirements Compared",
                len(semantic_results)
            )

            for index, item in enumerate(
                semantic_results,
                start=1
            ):

                with st.expander(
                    f"Requirement {index} — "
                    f"Similarity: {item['similarity']:.2f}"
                ):

                    st.markdown("**Job Requirement**")
                    st.write(item["job_requirement"])

                    st.markdown("**Closest Resume Evidence**")
                    st.write(item["resume_evidence"])

        else:

            st.info(
                "Not enough meaningful statements "
                "were available for semantic analysis."
            )


    # ======================================
    # TAB 5: REPORT
    # ======================================

    with report_tab:

        st.header("Resume Intelligence Report")

        st.write(
            "Download your context-aware skill analysis, "
            "priority gaps, and personalized learning roadmap."
        )

        if (
            "pdf_bytes" not in st.session_state
            and "pdf_error" not in st.session_state
        ):

            try:

                with st.spinner("Generating PDF report..."):

                    pdf_bytes = generate_pdf_report(
                        analysis,
                        priorities,
                        roadmap
                    )

                    if not isinstance(pdf_bytes, bytes):
                        raise ValueError(
                            "The PDF generator returned invalid data."
                        )

                    if not pdf_bytes.startswith(b"%PDF-"):
                        raise ValueError(
                            "The generated report is not a valid PDF."
                        )

                    st.session_state["pdf_bytes"] = pdf_bytes

            except Exception as error:

                st.session_state["pdf_error"] = str(error)

        if "pdf_bytes" in st.session_state:

            pdf_bytes = st.session_state["pdf_bytes"]

            st.success("PDF report is ready.")

            st.caption(
                f"File size: {len(pdf_bytes):,} bytes"
            )

            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="Resume_Intelligence_Report.pdf",
                mime="application/pdf",
                type="primary",
                key="final_pdf_download",
                on_click="ignore"
            )

        elif "pdf_error" in st.session_state:

            st.error("Unable to generate the PDF report.")

            with st.expander("PDF Error Details"):
                st.code(st.session_state["pdf_error"])

        st.divider()

        with st.expander("View Extracted Resume Text"):

            st.text_area(
                "Extracted Resume",
                value=resume_text,
                height=350,
                disabled=True
            )

            word_col, char_col = st.columns(2)

            with word_col:

                st.metric(
                    "Total Words",
                    len(resume_text.split())
                )

            with char_col:

                st.metric(
                    "Total Characters",
                    len(resume_text)
                )
