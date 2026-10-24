
from utils.context_resolver import resolve_skill_contexts
from utils.skill_extractor import extract_skills
from utils.skill_gap_analyzer import flatten_skills


def analyze_context_skill_gap(resume_text, job_description):
    """
    Calculate skill coverage using context-resolved
    resume skills instead of all keyword mentions.
    """

    # Get final classifications for resume skills
    context_result = resolve_skill_contexts(resume_text)

    resolved = context_result["resolved"]

    demonstrated = set(resolved["demonstrated"])
    learning = set(resolved["learning"])
    interested = set(resolved["interested"])
    negated = set(resolved["negated"])
    conflicting = set(resolved["conflicting"])

    # Extract skills requested by the job
    job_skills = flatten_skills(
        extract_skills(job_description)
    )

    # Only demonstrated skills count as matches
    matched = demonstrated & job_skills

    # Other mentioned skills are not counted as matches
    missing = job_skills - matched

    learning_gaps = missing & learning
    interest_gaps = missing & interested
    negated_gaps = missing & negated
    conflicting_gaps = missing & conflicting

    # Skills absent from the resume entirely
    unmentioned = missing - (
        learning_gaps
        | interest_gaps
        | negated_gaps
        | conflicting_gaps
    )

    if job_skills:
        score = round(
            100 * len(matched) / len(job_skills),
            2
        )
    else:
        score = None

    return {
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "learning_skills": sorted(learning_gaps),
        "interested_skills": sorted(interest_gaps),
        "negated_skills": sorted(negated_gaps),
        "conflicting_skills": sorted(conflicting_gaps),
        "unmentioned_skills": sorted(unmentioned),
        "match_score": score,
        "context_evidence": context_result["evidence"]
    }
