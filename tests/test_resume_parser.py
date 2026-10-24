
import pytest
import pymupdf

from io import BytesIO
from docx import Document

from utils.resume_parser import extract_resume_text


# ==========================================
# HELPER: SIMULATE STREAMLIT UPLOADED FILE
# ==========================================

class MockUploadedFile:

    def __init__(self, filename, content):
        self.name = filename
        self.content = content

    def getvalue(self):
        return self.content


# ==========================================
# HELPER: CREATE SAMPLE PDF
# ==========================================

def create_sample_pdf(text=None):

    document = pymupdf.open()

    page = document.new_page()

    if text:
        page.insert_text((72, 72), text)

    pdf_bytes = document.tobytes()

    document.close()

    return pdf_bytes


# ==========================================
# HELPER: CREATE SAMPLE DOCX
# ==========================================

def create_sample_docx(text=None):

    document = Document()

    if text:
        document.add_paragraph(text)

    buffer = BytesIO()

    document.save(buffer)

    return buffer.getvalue()


# ==========================================
# TEST 1: PDF TEXT EXTRACTION
# ==========================================

def test_pdf_extraction():

    pdf_bytes = create_sample_pdf(
        "Python Machine Learning SQL"
    )

    uploaded_file = MockUploadedFile(
        "resume.pdf",
        pdf_bytes
    )

    result = extract_resume_text(uploaded_file)

    assert "Python" in result
    assert "Machine Learning" in result
    assert "SQL" in result


# ==========================================
# TEST 2: DOCX TEXT EXTRACTION
# ==========================================

def test_docx_extraction():

    docx_bytes = create_sample_docx(
        "Python Git Docker"
    )

    uploaded_file = MockUploadedFile(
        "resume.docx",
        docx_bytes
    )

    result = extract_resume_text(uploaded_file)

    assert "Python" in result
    assert "Git" in result
    assert "Docker" in result


# ==========================================
# TEST 3: EMPTY PDF
# ==========================================

def test_empty_pdf():

    pdf_bytes = create_sample_pdf()

    uploaded_file = MockUploadedFile(
        "empty.pdf",
        pdf_bytes
    )

    result = extract_resume_text(uploaded_file)

    assert result == ""


# ==========================================
# TEST 4: EMPTY DOCX
# ==========================================

def test_empty_docx():

    docx_bytes = create_sample_docx()

    uploaded_file = MockUploadedFile(
        "empty.docx",
        docx_bytes
    )

    result = extract_resume_text(uploaded_file)

    assert result == ""


# ==========================================
# TEST 5: UNSUPPORTED FILE FORMAT
# ==========================================

def test_unsupported_file():

    uploaded_file = MockUploadedFile(
        "resume.txt",
        b"Python SQL"
    )

    with pytest.raises(ValueError):
        extract_resume_text(uploaded_file)


# ==========================================
# TEST 6: NO FILE PROVIDED
# ==========================================

def test_no_file():

    result = extract_resume_text(None)

    assert result == ""


# ==========================================
# TEST 7: CORRUPTED PDF
# ==========================================

def test_corrupted_pdf():

    uploaded_file = MockUploadedFile(
        "corrupted.pdf",
        b"This is not a real PDF file"
    )

    with pytest.raises(Exception):
        extract_resume_text(uploaded_file)


# ==========================================
# TEST 8: CORRUPTED DOCX
# ==========================================

def test_corrupted_docx():

    uploaded_file = MockUploadedFile(
        "corrupted.docx",
        b"This is not a real DOCX file"
    )

    with pytest.raises(Exception):
        extract_resume_text(uploaded_file)
