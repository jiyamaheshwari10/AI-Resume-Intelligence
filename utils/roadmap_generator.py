
import json
from pathlib import Path

from utils.skill_priority import prioritize_skill_gaps


BASE_DIR = Path(__file__).resolve().parent.parent

RESOURCES_PATH = (
    BASE_DIR / "data" / "learning_resources.json"
)


def load_learning_resources():
    with open(
        RESOURCES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def generate_learning_roadmap(
    resume_text,
    job_description
):
    """
    Generate a prioritized learning roadmap
    based on missing job skills.
    """

    skill_gaps = prioritize_skill_gaps(
        resume_text,
        job_description
    )

    resources = load_learning_resources()

    roadmap = []

    for index, gap in enumerate(skill_gaps, start=1):

        skill = gap["skill"]

        learning_data = resources.get(skill)

        if learning_data is None:
            learning_data = {
                "topics": [
                    f"Learn the fundamentals of {skill}",
                    f"Practice core concepts of {skill}",
                    f"Apply {skill} in a small project"
                ],
                "project": (
                    f"Build a beginner project using {skill}"
                ),
                "resource": None
            }

        roadmap.append({
            "step": index,
            "skill": skill,
            "priority": gap["priority"],
            "category": gap["category"],
            "topics": learning_data["topics"],
            "project": learning_data["project"],
            "resource": learning_data["resource"]
        })

    return roadmap
