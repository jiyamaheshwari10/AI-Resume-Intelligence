
from io import BytesIO

import pytest

from utils.input_validator import (
    InputValidationError,
    validate_resume,
    validate_job_description,
    MAX_FILE_SIZE
)


class MockUploadedFile:

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def getvalue(self):
        return self.content


def test_missing_resume():

    with pytest.raises(InputValidationError):
        validate_resume(None)


def test_unsupported_extension():

    file = MockUploadedFile(
        "resume.txt",
        b"Python developer resume"
    )

    with pytest.raises(InputValidationError):
        validate_resume(file)


def test_empty_file():

    file = MockUploadedFile(
        "resume.pdf",
        b""
    )

    with pytest.raises(InputValidationError):
        validate_resume(file)


def test_oversized_file():

    file = MockUploadedFile(
        "resume.pdf",
        b"x" * (MAX_FILE_SIZE + 1)
    )

    with pytest.raises(InputValidationError):
        validate_resume(file)


def test_corrupted_pdf():

    file = MockUploadedFile(
        "resume.pdf",
        b"Not a valid PDF"
    )

    with pytest.raises(InputValidationError):
        validate_resume(file)


def test_empty_job_description():

    with pytest.raises(InputValidationError):
        validate_job_description("")


def test_short_job_description():

    with pytest.raises(InputValidationError):
        validate_job_description(
            "Python SQL Git"
        )


def test_valid_job_description():

    job = (
        "We are looking for a Python developer "
        "with SQL, Git and machine learning experience."
    )

    result = validate_job_description(job)

    assert result == job


def test_job_description_trimming():

    job = (
        "   We need a Python developer with "
        "experience in SQL, Docker, Git and AWS.   "
    )

    result = validate_job_description(job)

    assert result == job.strip()
