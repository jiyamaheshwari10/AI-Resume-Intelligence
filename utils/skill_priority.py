
import re

from utils.skill_extractor import extract_skills
from utils.skill_gap_analyzer import flatten_skills


REQUIRED_KEYWORDS = [
    "required",
    "requirements",
    "must have",
    "mandatory",
    "essential",
    "minimum qualifications"
]

PREFERRED_KEYWORDS = [
    "preferred",
    "nice to have",
    "good to have",
    "desirable",
    "bonus",
    "optional"
]


def classify_job_skills(job_description):
    """
    Identify skills in required and preferred
    sections of a job description.
    """

    required_skills = set()
    preferred_skills = set()
    unclassified_skills = set()

    current_section = "unclassified"

    lines = job_description.splitlines()

    for line in lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        lower_line = cleaned_line.lower()

        required_found = any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                lower_line
            )
            for keyword in REQUIRED_KEYWORDS
        )

        preferred_found = any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                lower_line
            )
            for keyword in PREFERRED_KEYWORDS
        )

        if required_found and not preferred_found:
            current_section = "required"

        elif preferred_found and not required_found:
            current_section = "preferred"

        skills = flatten_skills(
            extract_skills(cleaned_line)
        )

        if current_section == "required":
            required_skills.update(skills)

        elif current_section == "preferred":
            preferred_skills.update(skills)

        else:
            unclassified_skills.update(skills)

    # Resolve repeated skills conservatively:
    # required takes precedence over preferred.
    preferred_skills -= required_skills
    unclassified_skills -= required_skills | preferred_skills

    return {
        "required": sorted(required_skills),
        "preferred": sorted(preferred_skills),
        "unclassified": sorted(unclassified_skills)
    }


def prioritize_skill_gaps(resume_text, job_description):
    """
    Rank missing skills based on how explicitly
    the job description classifies them.
    """

    resume_skills = flatten_skills(
        extract_skills(resume_text)
    )

    job_skills = classify_job_skills(job_description)

    priorities = []

    categories = [
        ("required", "High", 1),
        ("preferred", "Medium", 2),
        ("unclassified", "Unspecified", 3)
    ]

    for category, priority, rank in categories:

        for skill in job_skills[category]:

            if skill not in resume_skills:
                priorities.append({
                    "skill": skill,
                    "category": category,
                    "priority": priority,
                    "rank": rank
                })

    return sorted(
        priorities,
        key=lambda item: (item["rank"], item["skill"])
    )
