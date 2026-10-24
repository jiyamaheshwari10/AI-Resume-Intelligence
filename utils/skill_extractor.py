import json
import re
from pathlib import Path


# Locate the database relative to this Python file
BASE_DIR = Path(__file__).resolve().parent.parent
SKILLS_PATH = BASE_DIR / "data" / "skills.json"


def load_skills():
    with open(SKILLS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def contains_skill(text, skill_alias):
    """
    Check whether an alias appears as a standalone
    term rather than inside another word.
    """

    pattern = (
        r"(?<!\w)"
        + re.escape(skill_alias)
        + r"(?!\w)"
    )

    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_skills(text):
    """
    Extract skills and organize them by category.
    """

    skill_database = load_skills()
    extracted_skills = {}

    for category, skills in skill_database.items():

        matched_skills = []

        for skill_name, aliases in skills.items():

            if any(
                contains_skill(text, alias)
                for alias in aliases
            ):
                matched_skills.append(skill_name)

        if matched_skills:
            extracted_skills[category] = matched_skills

    return extracted_skills