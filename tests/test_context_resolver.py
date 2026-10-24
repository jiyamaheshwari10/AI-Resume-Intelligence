
from utils.context_resolver import resolve_skill_contexts


# ==========================================
# TEST 1: LEARNING + DEMONSTRATED
# ==========================================

def test_learning_then_demonstrated():

    resume = """
Currently learning Docker.
Built an application using Docker.
"""

    result = resolve_skill_contexts(resume)

    assert "Docker" in result["resolved"]["demonstrated"]
    assert "Docker" not in result["resolved"]["learning"]


# ==========================================
# TEST 2: INTEREST + LEARNING
# ==========================================

def test_interest_then_learning():

    resume = """
Interested in Kubernetes.
Currently learning Kubernetes.
"""

    result = resolve_skill_contexts(resume)

    assert "Kubernetes" in result["resolved"]["learning"]


# ==========================================
# TEST 3: NEGATED SKILL
# ==========================================

def test_negated_skill():

    resume = "No experience with AWS."

    result = resolve_skill_contexts(resume)

    assert "AWS" in result["resolved"]["negated"]


# ==========================================
# TEST 4: CONFLICTING EVIDENCE
# ==========================================

def test_conflicting_evidence():

    resume = """
No experience with AWS.
Deployed an application using AWS.
"""

    result = resolve_skill_contexts(resume)

    assert "AWS" in result["resolved"]["conflicting"]
    assert "AWS" in result["conflicts"]


# ==========================================
# TEST 5: TRACK ORIGINAL CONTEXTS
# ==========================================

def test_evidence_tracking():

    resume = """
Currently learning Docker.
Built a project using Docker.
"""

    result = resolve_skill_contexts(resume)

    assert result["evidence"]["Docker"] == [
        "demonstrated",
        "learning"
    ]


# ==========================================
# TEST 6: EMPTY RESUME
# ==========================================

def test_empty_resume():

    result = resolve_skill_contexts("")

    assert result["conflicts"] == []

    assert all(
        not skills
        for skills in result["resolved"].values()
    )
