
import time

from utils.semantic_matcher import find_semantic_matches


resume = """
Python developer with machine learning experience.

Developed a sentiment analysis model using Python.

Built a text classification application.

Worked with SQL databases and Git.
"""


job = """
We need a Python developer with machine learning experience.

Candidates should have experience in natural language
processing and text classification.

Knowledge of SQL, Git, Docker and AWS is preferred.
"""


print("Starting semantic matching...", flush=True)

start = time.perf_counter()

results = find_semantic_matches(resume, job)

elapsed = time.perf_counter() - start


print("\nResults:")

for result in results:
    print(
        result["job_requirement"],
        "->",
        result["similarity"]
    )

print(f"\nTotal execution time: {elapsed:.2f} seconds")

assert len(results) > 0

print("Semantic matching test passed!")
