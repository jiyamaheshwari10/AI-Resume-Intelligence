
from utils.skill_gap_analyzer import analyze_skill_gap
from utils.skill_priority import prioritize_skill_gaps

from utils.visualizer import (
    create_skill_coverage_chart,
    create_category_chart,
    create_priority_chart
)


resume_text = """
Python and Git
"""

job_description = """
Required:
Python
SQL
Machine Learning
Git

Preferred:
Docker
AWS
"""


analysis = analyze_skill_gap(
    resume_text,
    job_description
)

priorities = prioritize_skill_gaps(
    resume_text,
    job_description
)


coverage_fig = create_skill_coverage_chart(analysis)

category_fig = create_category_chart(
    resume_text,
    job_description
)

priority_fig = create_priority_chart(priorities)


assert coverage_fig is not None
assert category_fig is not None
assert priority_fig is not None

assert len(analysis["matched_skills"]) == 2
assert len(analysis["missing_skills"]) == 4

print("All visualization tests passed!")
