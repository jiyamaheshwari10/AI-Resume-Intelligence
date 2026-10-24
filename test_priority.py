
from utils.skill_priority import (
    classify_job_skills,
    prioritize_skill_gaps
)


resume_text = """
Experience with Python and Git.
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

classified = classify_job_skills(job_description)

print("Classified Job Skills:")
print(classified)

gaps = prioritize_skill_gaps(
    resume_text,
    job_description
)

print("\nPrioritized Skill Gaps:")

for gap in gaps:
    print(
        f"{gap['skill']} | "
        f"{gap['priority']} | "
        f"{gap['category']}"
    )


assert classified["required"] == [
    "Git", "Machine Learning", "Python", "SQL"
]

assert classified["preferred"] == [
    "AWS", "Docker"
]

assert [gap["skill"] for gap in gaps] == [
    "Machine Learning", "SQL", "AWS", "Docker"
]

print("\nAll priority tests passed!")
