from utils.skill_gap_analyzer import analyze_skill_gap

resume_text = """
I have experience with Python, SQL,
Machine Learning and Git.
"""

job_description = """
We require Python, SQL, Docker,
Git and AWS.
"""

result = analyze_skill_gap(
    resume_text,
    job_description
)

print("Matched:", result["matched_skills"])
print("Missing:", result["missing_skills"])
print("Additional:", result["additional_skills"])
print("Score:", result["match_score"])

assert result["match_score"] == 60.0
assert result["missing_skills"] == ["AWS", "Docker"]
assert result["matched_skills"] == ["Git", "Python", "SQL"]

print("All tests passed!")