
from utils.context_analyzer import analyze_skill_context


def resolve_skill_contexts(resume_text):
    """
    Resolve skills appearing in multiple contexts.

    Returns:
        resolved: skills grouped by final classification
        conflicts: skills with contradictory evidence
        evidence: original classifications per skill
    """

    contexts = analyze_skill_context(resume_text)

    # Group all detected contexts by skill
    evidence = {}

    for context, skills in contexts.items():
        for skill in skills:
            evidence.setdefault(skill, set()).add(context)

    resolved = {
        "demonstrated": [],
        "learning": [],
        "interested": [],
        "negated": [],
        "conflicting": []
    }

    conflicts = []

    for skill, skill_contexts in evidence.items():

        # Contradictory evidence
        if (
            "negated" in skill_contexts
            and "demonstrated" in skill_contexts
        ):
            classification = "conflicting"
            conflicts.append(skill)

        # Positive evidence takes precedence
        elif "demonstrated" in skill_contexts:
            classification = "demonstrated"

        # Learning takes precedence over interest
        elif "learning" in skill_contexts:
            classification = "learning"

        elif "interested" in skill_contexts:
            classification = "interested"

        else:
            classification = "negated"

        resolved[classification].append(skill)

    # Sort results for consistent output
    resolved = {
        category: sorted(skills)
        for category, skills in resolved.items()
    }

    formatted_evidence = {
        skill: sorted(contexts)
        for skill, contexts in evidence.items()
    }

    return {
        "resolved": resolved,
        "conflicts": sorted(conflicts),
        "evidence": formatted_evidence
    }
