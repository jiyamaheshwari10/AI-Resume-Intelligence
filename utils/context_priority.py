
from utils.context_skill_gap import analyze_context_skill_gap
from utils.skill_priority import classify_job_skills


def prioritize_context_gaps(resume_text, job_description):
    """
    Prioritize skills not evidenced as demonstrated
    in the resume, considering both job requirements
    and resume context.
    """

    analysis = analyze_context_skill_gap(
        resume_text,
        job_description
    )

    classifications = classify_job_skills(job_description)

    missing = set(analysis["missing_skills"])

    context_groups = {
        "learning": set(analysis["learning_skills"]),
        "interested": set(analysis["interested_skills"]),
        "negated": set(analysis["negated_skills"]),
        "conflicting": set(analysis["conflicting_skills"]),
        "unmentioned": set(analysis["unmentioned_skills"])
    }

    category_settings = [
        ("required", "High", 1),
        ("preferred", "Medium", 2),
        ("unclassified", "Unspecified", 3)
    ]

    priorities = []

    for category, priority, rank in category_settings:

        for skill in classifications[category]:

            if skill not in missing:
                continue

            skill_context = "unmentioned"

            for context, skills in context_groups.items():
                if skill in skills:
                    skill_context = context
                    break

            priorities.append({
                "skill": skill,
                "category": category,
                "priority": priority,
                "rank": rank,
                "context": skill_context
            })

    return sorted(
        priorities,
        key=lambda item: (
            item["rank"],
            item["skill"]
        )
    )
