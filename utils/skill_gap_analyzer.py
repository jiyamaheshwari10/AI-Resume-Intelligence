from utils.skill_extractor import extract_skills


def flatten_skills(skills_by_category):
    """
    Convert categorized skills into a single set.
    """
    return {
        skill
        for skill_list in skills_by_category.values()
        for skill in skill_list
    }


def analyze_skill_gap(resume_text, job_description):
    """
    Compare detected resume skills with job skills.
    """

    resume_skills = flatten_skills(
        extract_skills(resume_text)
    )

    job_skills = flatten_skills(
        extract_skills(job_description)
    )

    matched_skills = resume_skills.intersection(job_skills)

    missing_skills = job_skills.difference(resume_skills)

    additional_skills = resume_skills.difference(job_skills)

    if job_skills:
        match_score = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        match_score = None

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "additional_skills": sorted(additional_skills),
        "match_score": (
            round(match_score, 2)
            if match_score is not None
            else None
        )
    }