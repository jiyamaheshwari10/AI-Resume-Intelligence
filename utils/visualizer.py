
import pandas as pd

try:
    import plotly.express as px
except ImportError:
    px = None

from utils.skill_extractor import (
    load_skills,
    extract_skills
)
from utils.skill_gap_analyzer import flatten_skills


def create_skill_coverage_chart(analysis):
    """
    Show matched vs missing job skills.
    """

    if px is None:
        return None

    matched = len(analysis["matched_skills"])
    missing = len(analysis["missing_skills"])

    if matched + missing == 0:
        return None

    df = pd.DataFrame({
        "Status": ["Matched", "Missing"],
        "Count": [matched, missing]
    })

    fig = px.pie(
        df,
        names="Status",
        values="Count",
        hole=0.55,
        title="Skill Coverage",
        color="Status",
        color_discrete_map={
            "Matched": "#16a34a",
            "Missing": "#ef4444"
        }
    )

    fig.update_layout(
        legend_title_text="Skill Status"
    )

    return fig


def create_category_chart(resume_text, job_description):
    """
    Compare matched and missing skills
    across technical categories.
    """

    if px is None:
        return None

    resume_skills = flatten_skills(
        extract_skills(resume_text)
    )

    job_skills = flatten_skills(
        extract_skills(job_description)
    )

    database = load_skills()

    records = []

    for category, skills in database.items():

        category_skills = set(skills.keys())

        relevant = category_skills.intersection(
            job_skills
        )

        if not relevant:
            continue

        matched = len(
            relevant.intersection(resume_skills)
        )

        missing = len(relevant) - matched

        records.append({
            "Category": category,
            "Matched": matched,
            "Missing": missing
        })

    if not records:
        return None

    df = pd.DataFrame(records)

    df = df.melt(
        id_vars="Category",
        value_vars=["Matched", "Missing"],
        var_name="Status",
        value_name="Count"
    )

    fig = px.bar(
        df,
        x="Category",
        y="Count",
        color="Status",
        barmode="group",
        title="Job Skills by Category",
        color_discrete_map={
            "Matched": "#16a34a",
            "Missing": "#ef4444"
        }
    )

    fig.update_layout(
        xaxis_title="Skill Category",
        yaxis_title="Number of Skills"
    )

    return fig


def create_priority_chart(priorities):
    """
    Display missing skill counts by priority.
    """

    if px is None:
        return None

    counts = {
        "High": 0,
        "Medium": 0,
        "Unspecified": 0
    }

    for gap in priorities:
        priority = gap["priority"]

        if priority in counts:
            counts[priority] += 1

    if not any(counts.values()):
        return None

    df = pd.DataFrame({
        "Priority": list(counts.keys()),
        "Count": list(counts.values())
    })

    fig = px.bar(
        df,
        x="Priority",
        y="Count",
        color="Priority",
        title="Missing Skills by Priority",
        color_discrete_map={
            "High": "#ef4444",
            "Medium": "#f59e0b",
            "Unspecified": "#64748b"
        }
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Priority",
        yaxis_title="Number of Missing Skills"
    )

    return fig
