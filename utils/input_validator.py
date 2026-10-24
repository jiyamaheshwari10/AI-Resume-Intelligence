
from pathlib import Path

from utils.resume_parser import extract_resume_text


# Maximum supported file size: 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

MIN_JOB_WORDS = 10
MIN_RESUME_CHARACTERS = 30


class InputValidationError(ValueError):
    """Raised when user input fails validation."""
    pass


def validate_resume(file):
    """
    Validate uploaded resume and return
    its extracted text if valid.
    """

    if file is None:
        raise InputValidationError(
            "Please upload a resume."
        )

    filename = getattr(file, "name", "")

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise InputValidationError(
            "Unsupported file format. "
            "Please upload a PDF or DOCX file."
        )

    file_bytes = file.getvalue()

    if not file_bytes:
        raise InputValidationError(
            "The uploaded file is empty."
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise InputValidationError(
            "Resume exceeds the 5 MB limit."
        )

    try:
        resume_text = extract_resume_text(file)

    except Exception as error:
        raise InputValidationError(
            "Unable to read the uploaded document. "
            "It may be corrupted or invalid."
        ) from error

    if len(resume_text.strip()) < MIN_RESUME_CHARACTERS:
        raise InputValidationError(
            "The resume contains insufficient "
            "readable text. Please upload a "
            "text-based resume."
        )

    return resume_text


def validate_job_description(text):
    """
    Validate job description before analysis.
    """

    if not isinstance(text, str):
        raise InputValidationError(
            "Job description must be text."
        )

    cleaned_text = text.strip()

    if not cleaned_text:
        raise InputValidationError(
            "Please enter a job description."
        )

    word_count = len(cleaned_text.split())

    if word_count < MIN_JOB_WORDS:
        raise InputValidationError(
            "The job description is too short. "
            "Please provide at least 10 words "
            "describing the role or required skills."
        )

    if not any(char.isalpha() for char in cleaned_text):
        raise InputValidationError(
            "The job description must contain "
            "meaningful text."
        )

    return cleaned_text
