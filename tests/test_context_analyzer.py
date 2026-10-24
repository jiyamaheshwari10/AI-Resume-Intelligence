
from utils.context_analyzer import (
    analyze_skill_context,
    classify_context
)


def test_demonstrated_context():
    statement = "Developed applications using Python"

    assert classify_context(statement) == "demonstrated"


def test_learning_context():
    statement = "Currently learning Docker"

    assert classify_context(statement) == "learning"


def test_negated_context():
    statement = "No experience with AWS"

    assert classify_context(statement) == "negated"


def test_interested_context():
    statement = "Interested in Kubernetes"

    assert classify_context(statement) == "interested"


def test_complete_context_analysis():

    resume = """
Developed applications using Python
Currently learning Docker
No experience with AWS
Interested in Kubernetes
Experience using Git
"""

    result = analyze_skill_context(resume)

    assert "Python" in result["demonstrated"]
    assert "Docker" in result["learning"]
    assert "AWS" in result["negated"]
    assert "Kubernetes" in result["interested"]
    assert "Git" in result["demonstrated"]

from utils.context_analyzer import split_into_clauses


# Test 6: Split contrasting clauses
def test_clause_splitting():

    text = (
        "Experienced with Python and SQL "
        "but currently learning Docker and AWS"
    )

    clauses = split_into_clauses(text)

    assert len(clauses) == 2
    assert "Python" in clauses[0]
    assert "Docker" in clauses[1]


# Test 7: Mixed demonstrated and learning
def test_mixed_skill_context():

    resume = (
        "Experienced with Python and SQL, "
        "but currently learning Docker and AWS."
    )

    result = analyze_skill_context(resume)

    assert "Python" in result["demonstrated"]
    assert "SQL" in result["demonstrated"]

    assert "Docker" in result["learning"]
    assert "AWS" in result["learning"]

    assert "Docker" not in result["demonstrated"]


# Test 8: Demonstrated and negated
def test_mixed_negated_context():

    resume = (
        "Built applications with Python "
        "but have no experience with Kubernetes."
    )

    result = analyze_skill_context(resume)

    assert "Python" in result["demonstrated"]
    assert "Kubernetes" in result["negated"]


# Test 9: Multiple contrast clauses
def test_multiple_clauses():

    resume = (
        "Experienced in Python but learning Docker "
        "whereas AWS is an area I am interested in."
    )

    result = analyze_skill_context(resume)

    assert "Python" in result["demonstrated"]
    assert "Docker" in result["learning"]
    assert "AWS" in result["interested"]
