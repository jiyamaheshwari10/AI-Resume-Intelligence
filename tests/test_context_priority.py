
from utils.context_priority import prioritize_context_gaps


def test_learning_required_skill():

    resume = """
Experienced with Python.
Currently learning Docker.
"""

    job = """
Required:
Python
Docker
"""

    result = prioritize_context_gaps(resume, job)

    assert len(result) == 1
    assert result[0]["skill"] == "Docker"
    assert result[0]["priority"] == "High"
    assert result[0]["context"] == "learning"


def test_negated_required_skill():

    resume = """
Experience with Python.
No experience with AWS.
"""

    job = """
Required:
Python
AWS
"""

    result = prioritize_context_gaps(resume, job)

    assert len(result) == 1
    assert result[0]["skill"] == "AWS"
    assert result[0]["context"] == "negated"


def test_preferred_skill():

    resume = "Built applications using Python."

    job = """
Required:
Python

Preferred:
Docker
"""

    result = prioritize_context_gaps(resume, job)

    assert len(result) == 1
    assert result[0]["skill"] == "Docker"
    assert result[0]["priority"] == "Medium"
    assert result[0]["context"] == "unmentioned"


def test_conflicting_skill():

    resume = """
No experience with AWS.
Deployed an application using AWS.
"""

    job = """
Required:
AWS
"""

    result = prioritize_context_gaps(resume, job)

    assert len(result) == 1
    assert result[0]["context"] == "conflicting"


def test_demonstrated_skill_excluded():

    resume = """
Built a Python application.
Worked with SQL databases.
"""

    job = """
Required:
Python
SQL
"""

    result = prioritize_context_gaps(resume, job)

    assert result == []


def test_priority_order():

    resume = "Experience with Python."

    job = """
Required:
Python
SQL

Preferred:
Docker
AWS
"""

    result = prioritize_context_gaps(resume, job)

    assert [item["skill"] for item in result] == [
        "SQL",
        "AWS",
        "Docker"
    ]

    assert [item["priority"] for item in result] == [
        "High",
        "Medium",
        "Medium"
    ]
