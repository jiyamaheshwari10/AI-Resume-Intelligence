
from utils.context_skill_gap import analyze_context_skill_gap


def test_context_aware_match_score():

    resume = """
Experienced with Python and SQL.
Currently learning Docker.
No experience with AWS.
Interested in Kubernetes.
"""

    job = """
Required:
Python
SQL
Docker
AWS
Kubernetes
"""

    result = analyze_context_skill_gap(resume, job)

    assert result["match_score"] == 40.0

    assert result["matched_skills"] == [
        "Python", "SQL"
    ]

    assert result["learning_skills"] == ["Docker"]
    assert result["negated_skills"] == ["AWS"]
    assert result["interested_skills"] == ["Kubernetes"]


def test_conflicting_skill_not_matched():

    resume = """
No experience with AWS.
Deployed a project using AWS.
"""

    job = "AWS"

    result = analyze_context_skill_gap(resume, job)

    assert result["match_score"] == 0.0
    assert result["conflicting_skills"] == ["AWS"]
    assert result["matched_skills"] == []


def test_learning_skill_not_matched():

    resume = "Currently learning Docker."

    job = "Docker"

    result = analyze_context_skill_gap(resume, job)

    assert result["match_score"] == 0.0
    assert result["learning_skills"] == ["Docker"]


def test_demonstrated_skill_matched():

    resume = "Built an application using Python."

    job = "Python"

    result = analyze_context_skill_gap(resume, job)

    assert result["match_score"] == 100.0
    assert result["matched_skills"] == ["Python"]


def test_unmentioned_skill():

    resume = "Experience using Python."

    job = "Python Docker"

    result = analyze_context_skill_gap(resume, job)

    assert result["match_score"] == 50.0
    assert result["unmentioned_skills"] == ["Docker"]


def test_empty_job_description():

    result = analyze_context_skill_gap(
        "Experience using Python.",
        ""
    )

    assert result["match_score"] is None
    assert result["job_skills"] == []
    assert result["missing_skills"] == []
