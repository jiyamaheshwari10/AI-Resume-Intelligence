
from utils.context_priority import prioritize_context_gaps
from utils.roadmap_generator import load_learning_resources


CONTEXT_ACTIONS = {
    "learning": {
        "status": "Already learning",
        "action": "Continue learning and build practical experience",
        "guidance": (
            "Review your current progress, complete the "
            "remaining topics, and demonstrate the skill "
            "through a practical project."
        )
    },
    "interested": {
        "status": "Interested",
        "action": "Explore the fundamentals",
        "guidance": (
            "Start with an introductory resource and "
            "complete a small practical exercise before "
            "committing to a larger project."
        )
    },
    "negated": {
        "status": "No experience stated",
        "action": "Start with fundamentals",
        "guidance": (
            "Begin with foundational concepts and gradually "
            "develop hands-on experience."
        )
    },
    "conflicting": {
        "status": "Conflicting evidence",
        "action": "Clarify experience before planning",
        "guidance": (
            "Your resume contains both positive and negative "
            "statements about this skill. Review the wording "
            "and assess your actual experience. If a gap "
            "remains, follow the recommended learning topics."
        )
    },
    "unmentioned": {
        "status": "Not mentioned in resume",
        "action": "Assess existing knowledge, then learn",
        "guidance": (
            "This skill was not detected in your resume. "
            "If you already know it, consider adding "
            "accurate evidence. Otherwise, begin learning."
        )
    }
}


def generate_context_roadmap(resume_text, job_description):
    """
    Build a prioritized learning roadmap using
    job requirements and resolved resume context.
    """

    priorities = prioritize_context_gaps(
        resume_text,
        job_description
    )

    resources = load_learning_resources()

    roadmap = []

    for index, gap in enumerate(priorities, start=1):

        skill = gap["skill"]
        context = gap["context"]

        learning_data = resources.get(skill, {
            "topics": [
                f"Understand the fundamentals of {skill}",
                f"Practice core concepts of {skill}",
                f"Build a small project using {skill}"
            ],
            "project": f"Create a practical project using {skill}",
            "resource": None
        })

        context_data = CONTEXT_ACTIONS[context]

        roadmap.append({
            "step": index,
            "skill": skill,
            "priority": gap["priority"],
            "category": gap["category"],
            "context": context,
            "status": context_data["status"],
            "action": context_data["action"],
            "guidance": context_data["guidance"],
            "topics": learning_data["topics"],
            "project": learning_data["project"],
            "resource": learning_data["resource"]
        })

    return roadmap
