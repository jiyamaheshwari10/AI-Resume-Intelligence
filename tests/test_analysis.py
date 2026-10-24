
from utils.skill_extractor import extract_skills


# Test 1: Empty resume
def test_empty_resume():

    result = extract_skills("")

    assert result == {}


# Test 2: Skill aliases
def test_skill_aliases():

    text = "Experience with ML, NLP and sklearn."

    result = extract_skills(text)

    ai_skills = result["AI and Data Science"]

    assert "Machine Learning" in ai_skills
    assert "Natural Language Processing" in ai_skills
    assert "Scikit-learn" in ai_skills


# Test 3: Prevent incorrect matching
def test_javascript_not_java():

    text = "Developed applications using JavaScript."

    result = extract_skills(text)

    programming = result["Programming Languages"]

    assert "JavaScript" in programming
    assert "Java" not in programming


# Test 4: Duplicate skill detection
def test_duplicate_skills():

    text = "Python Python Python SQL SQL"

    result = extract_skills(text)

    programming = result["Programming Languages"]

    assert programming.count("Python") == 1
    assert programming.count("SQL") == 1

# ==========================================
# SKILL GAP ANALYZER TESTS
# ==========================================

from utils.skill_gap_analyzer import analyze_skill_gap


# Test 5: Correct skill match score
def test_skill_match_score():

    resume = "Python SQL Git"

    job = "Python SQL Git Docker AWS"

    result = analyze_skill_gap(resume, job)

    assert result["match_score"] == 60.0


# Test 6: Correct matched and missing skills
def test_matched_and_missing_skills():

    resume = "Python SQL Git"

    job = "Python SQL Git Docker AWS"

    result = analyze_skill_gap(resume, job)

    assert result["matched_skills"] == [
        "Git", "Python", "SQL"
    ]

    assert result["missing_skills"] == [
        "AWS", "Docker"
    ]


# Test 7: Perfect skill match
def test_perfect_skill_match():

    resume = "Python SQL Git"

    job = "Python SQL"

    result = analyze_skill_gap(resume, job)

    assert result["match_score"] == 100.0
    assert result["missing_skills"] == []


# Test 8: No recognized job skills
def test_no_recognized_job_skills():

    resume = "Python SQL"

    job = "Excellent communication and teamwork."

    result = analyze_skill_gap(resume, job)

    assert result["match_score"] is None
    assert result["job_skills"] == []


# Test 9: Empty resume
def test_empty_resume_skill_gap():

    resume = ""

    job = "Python SQL Git"

    result = analyze_skill_gap(resume, job)

    assert result["match_score"] == 0.0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == [
        "Git", "Python", "SQL"
    ]


# Test 10: Empty documents
def test_empty_documents_skill_gap():

    result = analyze_skill_gap("", "")

    assert result["match_score"] is None
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []

# ==========================================
# SKILL PRIORITIZATION & ROADMAP TESTS
# ==========================================

from utils.skill_priority import (
    classify_job_skills,
    prioritize_skill_gaps
)

from utils.roadmap_generator import generate_learning_roadmap


# Test 11: Required vs preferred skills
def test_required_preferred_classification():

    job = """
Required:
Python
SQL
Machine Learning

Preferred:
Docker
AWS
"""

    result = classify_job_skills(job)

    assert result["required"] == [
        "Machine Learning", "Python", "SQL"
    ]

    assert result["preferred"] == [
        "AWS", "Docker"
    ]


# Test 12: Required skills have higher priority
def test_skill_priority_order():

    resume = "Python and Git"

    job = """
Required:
Python
SQL
Git

Preferred:
Docker
AWS
"""

    gaps = prioritize_skill_gaps(resume, job)

    assert gaps[0]["skill"] == "SQL"
    assert gaps[0]["priority"] == "High"

    assert all(
        gap["priority"] == "Medium"
        for gap in gaps[1:]
    )


# Test 13: Already possessed skills excluded
def test_existing_skills_not_prioritized():

    resume = "Python, SQL and Git"

    job = """
Required:
Python
SQL
Git
Docker
"""

    gaps = prioritize_skill_gaps(resume, job)

    assert len(gaps) == 1
    assert gaps[0]["skill"] == "Docker"


# Test 14: Roadmap generation
def test_roadmap_generation():

    resume = "Python"

    job = """
Required:
Python
SQL

Preferred:
Docker
"""

    roadmap = generate_learning_roadmap(
        resume,
        job
    )

    assert len(roadmap) == 2

    assert roadmap[0]["skill"] == "SQL"
    assert roadmap[0]["priority"] == "High"

    assert roadmap[1]["skill"] == "Docker"
    assert roadmap[1]["priority"] == "Medium"


# Test 15: Learning resources available
def test_learning_resources():

    resume = "Python"

    job = """
Required:
Python
SQL
"""

    roadmap = generate_learning_roadmap(
        resume,
        job
    )

    sql_step = roadmap[0]

    assert sql_step["skill"] == "SQL"
    assert len(sql_step["topics"]) > 0
    assert sql_step["project"]
    assert sql_step["resource"]


# Test 16: No missing skills
def test_no_learning_gaps():

    resume = "Python SQL Git"

    job = """
Required:
Python
SQL
Git
"""

    roadmap = generate_learning_roadmap(
        resume,
        job
    )

    assert roadmap == []
