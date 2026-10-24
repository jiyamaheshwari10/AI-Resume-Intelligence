
import pytest
import pymupdf

from utils.skill_gap_analyzer import analyze_skill_gap
from utils.skill_priority import prioritize_skill_gaps
from utils.roadmap_generator import generate_learning_roadmap
from utils.report_generator import generate_pdf_report


# ==========================================
# SAMPLE DATA
# ==========================================

@pytest.fixture
def report_data():

    resume = "Python and Git"

    job = """
Required:
Python
SQL
Machine Learning
Git

Preferred:
Docker
AWS
"""

    analysis = analyze_skill_gap(resume, job)

    priorities = prioritize_skill_gaps(resume, job)

    roadmap = generate_learning_roadmap(resume, job)

    return analysis, priorities, roadmap


# ==========================================
# HELPER: EXTRACT GENERATED PDF TEXT
# ==========================================

def extract_pdf_text(pdf_bytes):

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        return "\n".join(
            page.get_text()
            for page in document
        )


# ==========================================
# TEST 1: PDF FILE SIGNATURE
# ==========================================

def test_pdf_signature(report_data):

    pdf_bytes = generate_pdf_report(*report_data)

    assert pdf_bytes.startswith(b"%PDF-")


# ==========================================
# TEST 2: PDF CAN BE OPENED
# ==========================================

def test_pdf_can_be_opened(report_data):

    pdf_bytes = generate_pdf_report(*report_data)

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        assert document.page_count >= 1


# ==========================================
# TEST 3: CORRECT REPORT TITLE
# ==========================================

def test_report_title(report_data):

    pdf_bytes = generate_pdf_report(*report_data)

    text = extract_pdf_text(pdf_bytes)

    assert "AI Resume Intelligence Report" in text


# ==========================================
# TEST 4: CORRECT MATCH SCORE
# ==========================================

def test_report_match_score(report_data):

    pdf_bytes = generate_pdf_report(*report_data)

    text = extract_pdf_text(pdf_bytes)

    assert "33.3%" in text


# ==========================================
# TEST 5: MISSING SKILLS INCLUDED
# ==========================================

def test_missing_skills_in_report(report_data):

    pdf_bytes = generate_pdf_report(*report_data)

    text = extract_pdf_text(pdf_bytes)

    for skill in [
        "SQL",
        "Machine Learning",
        "Docker",
        "AWS"
    ]:
        assert skill in text


# ==========================================
# TEST 6: LEARNING ROADMAP INCLUDED
# ==========================================

def test_learning_roadmap_in_report(report_data):

    pdf_bytes = generate_pdf_report(*report_data)

    text = extract_pdf_text(pdf_bytes)

    assert "Personalized Learning Roadmap" in text
    assert "Practice Project:" in text
    assert "Step 1:" in text


# ==========================================
# TEST 7: EMPTY SKILL GAP REPORT
# ==========================================

def test_no_missing_skills_report():

    resume = "Python SQL Git"
    job = "Python SQL Git"

    analysis = analyze_skill_gap(resume, job)

    priorities = prioritize_skill_gaps(resume, job)

    roadmap = generate_learning_roadmap(resume, job)

    pdf_bytes = generate_pdf_report(
        analysis,
        priorities,
        roadmap
    )

    text = extract_pdf_text(pdf_bytes)

    assert "100.0%" in text
    assert "No missing recognized skills detected." in text
    assert "No learning gaps identified." in text


# ==========================================
# TEST 8: UNAVAILABLE MATCH SCORE
# ==========================================

def test_unavailable_score_report():

    resume = "Python SQL"
    job = "Excellent communication and teamwork."

    analysis = analyze_skill_gap(resume, job)

    priorities = prioritize_skill_gaps(resume, job)

    roadmap = generate_learning_roadmap(resume, job)

    pdf_bytes = generate_pdf_report(
        analysis,
        priorities,
        roadmap
    )

    text = extract_pdf_text(pdf_bytes)

    assert "Not available" in text

from utils.intelligence_engine import generate_intelligence_results


def test_context_aware_pdf_content():

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

    pdf_bytes = generate_pdf_report(
        result["analysis"],
        result["priorities"],
        result["roadmap"]
    )

    text = extract_pdf_text(pdf_bytes)

    assert "50.0%" in text
    assert "Currently Learning: Docker" in text
    assert "No Experience Stated: AWS" in text
    assert "Recommended Action:" in text
    assert "Personalized Learning Roadmap" in text
