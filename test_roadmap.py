
from utils.roadmap_generator import (
    generate_learning_roadmap
)


resume_text = """
I have experience with Python and Git.
"""

job_description = """
Required:
Python
SQL
Machine Learning
Git

Preferred:
Docker
AWS
"""


roadmap = generate_learning_roadmap(
    resume_text,
    job_description
)


for item in roadmap:

    print("\n------------------------")
    print("Step:", item["step"])
    print("Skill:", item["skill"])
    print("Priority:", item["priority"])

    print("Topics:")

    for topic in item["topics"]:
        print("-", topic)

    print("Project:", item["project"])
    print("Resource:", item["resource"])


assert len(roadmap) == 4

assert [item["skill"] for item in roadmap] == [
    "Machine Learning",
    "SQL",
    "AWS",
    "Docker"
]

assert roadmap[0]["priority"] == "High"

assert roadmap[-1]["priority"] == "Medium"

assert roadmap[1]["project"] == (
    "Build a student records database"
)

print("\nAll roadmap tests passed!")
