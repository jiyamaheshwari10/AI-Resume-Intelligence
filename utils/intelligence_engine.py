
from utils.skill_extractor import extract_skills
from utils.skill_gap_analyzer import flatten_skills

from utils.context_skill_gap import analyze_context_skill_gap
from utils.context_priority import prioritize_context_gaps
from utils.context_roadmap import generate_context_roadmap
from utils.context_resolver import resolve_skill_contexts
from utils.skill_priority import classify_job_skills


def generate_intelligence_results(resume_text, job_description):
    """
    Generate consistent context-aware results
    for the dashboard, charts and PDF report.
    """

    # Extract all mentioned technical skills
    detected_skills = extract_skills(resume_text)

    # Resolve skill contexts
    context_results = resolve_skill_contexts(resume_text)

    # Calculate context-aware skill coverage
    analysis = analyze_context_skill_gap(
        resume_text,
        job_description
    )

    # Identify skill priorities
    priorities = prioritize_context_gaps(
        resume_text,
        job_description
    )

    # Generate personalized learning roadmap
    roadmap = generate_context_roadmap(
        resume_text,
        job_description
    )

    # Classify job requirements
    classified = classify_job_skills(job_description)

    # Additional skills should only include skills
    # treated as demonstrated by our context rules
    demonstrated = set(
        context_results["resolved"]["demonstrated"]
    )

    job_skills = set(analysis["job_skills"])

    additional_skills = sorted(
        demonstrated - job_skills
    )

    # Maintain compatibility with our PDF generator
    analysis["additional_skills"] = additional_skills

    return {
        "skills": detected_skills,
        "context_results": context_results,
        "analysis": analysis,
        "priorities": priorities,
        "roadmap": roadmap,
        "classified": classified
    }
