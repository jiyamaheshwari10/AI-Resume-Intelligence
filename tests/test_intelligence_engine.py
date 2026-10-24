
from utils.intelligence_engine import generate_intelligence_results


def test_context_aware_score():

    resume = """
Experienced with Python and SQL.
Currently learning Docker.
No experience with AWS.
"""

    job = """
Required:
Python
SQL
Docker
AWS
"""

    result = generate_intelligence_results(
        resume,
        job
    )

    analysis = result["analysis"]

    assert analysis["match_score"] == 50.0

    assert analysis["matched_skills"] == [
        "Python",
        "SQL"
    ]

    assert "Docker" in analysis["learning_skills"]

    assert "AWS" in analysis["negated_skills"]


def test_priorities_and_roadmap_consistency():

    resume = """
Experienced with Python.
Currently learning Docker.
"""

    job = """
Required:
Python
Docker
SQL
"""

    result = generate_intelligence_results(
        resume,
        job
    )

    priority_skills = [
        item["skill"]
        for item in result["priorities"]
    ]

    roadmap_skills = [
        item["skill"]
        for item in result["roadmap"]
    ]

    assert priority_skills == roadmap_skills

    assert "Docker" in priority_skills
    assert "SQL" in priority_skills

    assert "Python" not in priority_skills


def test_pdf_report_compatibility():

    resume = "Experienced with Python and Git."

    job = """
Required:
Python
SQL
"""

    result = generate_intelligence_results(
        resume,
        job
    )

    analysis = result["analysis"]

    assert "additional_skills" in analysis
    assert "Git" in analysis["additional_skills"]

    assert "match_score" in analysis
    assert "missing_skills" in analysis


def test_no_job_skills():

    result = generate_intelligence_results(
        "Experienced with Python.",
        "Excellent communication and teamwork."
    )

    assert result["analysis"]["match_score"] is None
    assert result["priorities"] == []
    assert result["roadmap"] == []


def test_empty_resume():

    result = generate_intelligence_results(
        "",
        "Required: Python and SQL"
    )

    assert result["analysis"]["match_score"] == 0.0

    assert result["analysis"]["matched_skills"] == []

    assert result["analysis"]["missing_skills"] == [
        "Python",
        "SQL"
    ]
