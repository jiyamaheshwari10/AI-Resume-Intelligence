
import re
import time

import numpy as np
import streamlit as st

from sentence_transformers import SentenceTransformer


# ==========================================
# 1. MODEL CONFIGURATION
# ==========================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

MAX_RESUME_STATEMENTS = 100
MAX_JOB_STATEMENTS = 30

BATCH_SIZE = 16


# ==========================================
# 2. LOAD AI MODEL
# ==========================================

@st.cache_resource(show_spinner=False)
def load_model():
    """
    Load the Sentence Transformer model.

    First try loading from the local cache.

    If the model is not cached, download it
    automatically and cache it for future use.
    """

    try:
        model = SentenceTransformer(
            MODEL_NAME,
            device="cpu",
            local_files_only=True
        )

    except OSError:
        model = SentenceTransformer(
            MODEL_NAME,
            device="cpu",
            local_files_only=False
        )

    return model


# ==========================================
# 3. SPLIT TEXT INTO STATEMENTS
# ==========================================

def split_into_statements(text):
    """
    Split text into meaningful statements.

    Supports line breaks and sentence-ending
    punctuation.
    """

    if not text or not text.strip():
        return []

    parts = re.split(r"[\n.!?;]+", text)

    statements = []

    for part in parts:

        statement = part.strip(" \t\r-•")

        if len(statement) >= 3:
            statements.append(statement)

    return statements


# ==========================================
# 4. COMPUTE SEMANTIC SIMILARITY
# ==========================================

def semantic_similarity(text1, text2):
    """
    Calculate semantic similarity between
    two pieces of text.

    Returns a cosine similarity score.
    """

    if not text1.strip() or not text2.strip():
        return 0.0

    model = load_model()

    embeddings = model.encode(
        [text1, text2],
        batch_size=BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    similarity = float(
        np.dot(embeddings[0], embeddings[1])
    )

    return similarity


# ==========================================
# 5. FIND SEMANTIC MATCHES
# ==========================================

def find_semantic_matches(
    resume_text,
    job_description
):
    """
    Compare job requirements against resume
    statements using Sentence Transformers.

    Returns the closest matching resume
    statement for each job requirement.
    """

    resume_statements = split_into_statements(
        resume_text
    )[:MAX_RESUME_STATEMENTS]

    job_statements = split_into_statements(
        job_description
    )[:MAX_JOB_STATEMENTS]

    if not resume_statements or not job_statements:
        return []

    start_time = time.perf_counter()

    model = load_model()

    resume_embeddings = model.encode(
        resume_statements,
        batch_size=BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    job_embeddings = model.encode(
        job_statements,
        batch_size=BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    # Cosine similarity for normalized embeddings
    similarity_matrix = np.matmul(
        job_embeddings,
        resume_embeddings.T
    )

    results = []

    for index, job_statement in enumerate(
        job_statements
    ):

        similarities = similarity_matrix[index]

        best_match_index = int(
            np.argmax(similarities)
        )

        best_score = float(
            similarities[best_match_index]
        )

        results.append({
            "job_requirement": job_statement,
            "resume_evidence": resume_statements[
                best_match_index
            ],
            "similarity": round(best_score, 4)
        })

    elapsed_time = time.perf_counter() - start_time

    return results
