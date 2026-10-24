
from utils.semantic_matcher import semantic_similarity


resume_statement = (
    "Built a machine learning model to classify "
    "customer feedback as positive or negative."
)

related_job_requirement = (
    "Experience developing sentiment analysis "
    "systems for customer reviews."
)

unrelated_job_requirement = (
    "Experience managing cloud infrastructure "
    "and configuring network security."
)


related_score = semantic_similarity(
    resume_statement,
    related_job_requirement
)

unrelated_score = semantic_similarity(
    resume_statement,
    unrelated_job_requirement
)


print("Related Similarity:", related_score)
print("Unrelated Similarity:", unrelated_score)


assert related_score > unrelated_score

print("Semantic matching test passed!")
