
import re

from utils.skill_extractor import (
    load_skills,
    contains_skill
)


# ==========================================
# CONTEXT PATTERNS
# ==========================================

NEGATED_PATTERNS = [
    r"\bno experience (?:with|in|using)\b",
    r"\bnot familiar with\b",
    r"\bnever (?:used|worked with)\b",
    r"\black (?:experience|knowledge) (?:with|in|of)\b"
]

LEARNING_PATTERNS = [
    r"\bcurrently learning\b",
    r"\blearning\b",
    r"\bstudying\b",
    r"\bplanning to learn\b"
]

INTEREST_PATTERNS = [
    r"\binterested in\b",
    r"\bwant to learn\b",
    r"\blooking to learn\b",
    r"\bexploring\b"
]


# ==========================================
# CLASSIFY INDIVIDUAL CLAUSE
# ==========================================

def classify_context(statement):

    text = statement.lower()

    for pattern in NEGATED_PATTERNS:
        if re.search(pattern, text):
            return "negated"

    for pattern in LEARNING_PATTERNS:
        if re.search(pattern, text):
            return "learning"

    for pattern in INTEREST_PATTERNS:
        if re.search(pattern, text):
            return "interested"

    return "demonstrated"


# ==========================================
# SPLIT SENTENCE INTO CLAUSES
# ==========================================

def split_into_clauses(statement):
    """
    Divide sentences at contrast words
    and punctuation.
    """

    clauses = re.split(
        r"\s+(?:but|however|whereas|while)\s+|[;.!?]",
        statement,
        flags=re.IGNORECASE
    )

    return [
        clause.strip()
        for clause in clauses
        if clause.strip()
    ]


# ==========================================
# ANALYZE EACH SKILL CONTEXT
# ==========================================

def analyze_skill_context(resume_text):

    skill_database = load_skills()

    results = {
        "demonstrated": set(),
        "learning": set(),
        "interested": set(),
        "negated": set()
    }

    for line in resume_text.splitlines():

        for clause in split_into_clauses(line):

            context = classify_context(clause)

            for category, skills in skill_database.items():

                for skill_name, aliases in skills.items():

                    if any(
                        contains_skill(clause, alias)
                        for alias in aliases
                    ):
                        results[context].add(skill_name)

    return {
        category: sorted(skills)
        for category, skills in results.items()
    }
