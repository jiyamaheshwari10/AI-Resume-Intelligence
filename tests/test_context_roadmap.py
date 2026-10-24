
from utils.context_roadmap import generate_context_roadmap


def test_learning_skill_guidance():

    resume = """
Experienced with Python.
Currently learning Docker.
"""

    job = """
Required:
Python
Docker
"""

    roadmap = generate_context_roadmap(resume, job)

    assert len(roadmap) == 1

    assert roadmap[0]["skill"] == "Docker"
    assert roadmap[0]["context"] == "learning"
    assert roadmap[0]["status"] == "Already learning"
    assert "Continue learning" in roadmap[0]["action"]


def test_negated_skill_guidance():

    resume = "No experience with AWS."

    job = """
Required:
AWS
"""

    roadmap = generate_context_roadmap(resume, job)

    assert roadmap[0]["context"] == "negated"
    assert roadmap[0]["action"] == "Start with fundamentals"


def test_unmentioned_skill_guidance():

    resume = "Experienced with Python."

    job = """
Required:
Python
SQL
"""

    roadmap = generate_context_roadmap(resume, job)

    assert len(roadmap) == 1
    assert roadmap[0]["skill"] == "SQL"
    assert roadmap[0]["context"] == "unmentioned"


def test_conflicting_skill_guidance():

    resume = """
No experience with AWS.
Deployed an application using AWS.
"""

    job = """
Required:
AWS
"""

    roadmap = generate_context_roadmap(resume, job)

    assert len(roadmap) == 1
    assert roadmap[0]["context"] == "conflicting"
    assert "Clarify" in roadmap[0]["action"]


def test_priority_order():

    resume = "Experienced with Python."

    job = """
Required:
Python
SQL

Preferred:
Docker
AWS
"""

    roadmap = generate_context_roadmap(resume, job)

    assert [item["skill"] for item in roadmap] == [
        "SQL",
        "AWS",
        "Docker"
    ]

    assert roadmap[0]["priority"] == "High"
    assert roadmap[1]["priority"] == "Medium"


def test_resources_and_projects():

    resume = "Experienced with Python."

    job = """
Required:
Python
SQL
"""

    roadmap = generate_context_roadmap(resume, job)

    sql_step = roadmap[0]

    assert len(sql_step["topics"]) > 0
    assert sql_step["project"] == (
        "Build a student records database"
    )
    assert sql_step["resource"]


def test_no_gaps():

    resume = "Experienced with Python and SQL."

    job = """
Required:
Python
SQL
"""

    roadmap = generate_context_roadmap(resume, job)

    assert roadmap == []
