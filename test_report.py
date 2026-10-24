
from pathlib import Path

from utils.skill_gap_analyzer import analyze_skill_gap
from utils.skill_priority import prioritize_skill_gaps
from utils.roadmap_generator import generate_learning_roadmap
from utils.report_generator import generate_pdf_report


resume_text = """
Python Developer with experience using
Python and Git for software projects.
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

roadmap = generate_learning_roadmap(
    resume_text,
    job_description
)


pdf_bytes = generate_pdf_report(
    analysis,
    priorities,
    roadmap
)


output_path = Path("test_resume_report.pdf")

output_path.write_bytes(pdf_bytes)


assert pdf_bytes.startswith(b"%PDF-")
assert len(pdf_bytes) > 1000
assert output_path.exists()

print("PDF report generated successfully!")
print("File:", output_path.resolve())
print("PDF size:", len(pdf_bytes), "bytes")
print("All report tests passed!")
