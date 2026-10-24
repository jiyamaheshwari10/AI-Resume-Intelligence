
# AI-Powered Resume Intelligence & Skill Gap Analyzer

An intelligent, context-aware resume analysis application that compares a candidate's technical skills with job requirements, identifies skill gaps, and generates personalized learning roadmaps.

Built using Python, Streamlit, NLP, and Sentence Transformers.

## Overview

Traditional keyword-based resume matching can identify whether a skill appears in a resume, but may fail to understand how that skill is mentioned.

For example:

- "Experienced with Docker"
- "Currently learning Docker"
- "No experience with Docker"

All three statements contain the same keyword but communicate different levels of experience.

This project introduces context-aware skill classification alongside semantic similarity analysis to provide more meaningful comparisons between resumes and job descriptions.

## Key Features

### Resume Processing
- Supports PDF and DOCX resumes
- Extracts resume text automatically
- Validates input format, file size, and content

### Skill Identification
- Extracts technical skills using a categorized skill database
- Supports skill aliases
- Identifies skills mentioned in job descriptions

### Context-Aware Skill Analysis
Classifies resume skills into:

- Demonstrated
- Currently Learning
- Interested
- Negated
- Conflicting Evidence

Uses rule-based language analysis to differentiate experience statements from learning goals and negative claims.

### Skill Gap Analysis
- Compares resume skills against job requirements
- Calculates keyword-based coverage
- Calculates context-aware skill coverage
- Identifies matched and missing skills
- Groups gaps by resume context

### AI Semantic Matching
- Uses Sentence Transformers
- Compares job requirements with resume statements
- Finds the most semantically similar resume evidence
- Uses the all-MiniLM-L6-v2 model

### Skill Prioritization
- Identifies required and preferred job skills
- Organizes skill gaps by priority
- Highlights areas requiring attention

### Personalized Learning Roadmap
- Generates learning steps for identified gaps
- Suggests topics to study
- Recommends practice projects
- Provides learning resources
- Adjusts guidance based on skill context

### Interactive Dashboard
- Built with Streamlit and Plotly
- Organized into five navigation tabs
- Includes coverage, priority, and category charts

### PDF Reporting
Generates a downloadable PDF report containing:

- Analysis summary
- Skill coverage
- Context classifications
- Gap priorities
- Personalized learning recommendations

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Streamlit | Interactive web interface |
| Sentence Transformers | Semantic text similarity |
| PyTorch | Model inference |
| NumPy | Numerical operations |
| Pandas | Data processing |
| Plotly | Interactive charts |
| PyMuPDF | PDF resume extraction |
| python-docx | DOCX resume extraction |
| ReportLab | PDF report generation |
| Pytest | Automated testing |

## How It Works

1. The user uploads a PDF or DOCX resume.
2. The user provides a job description.
3. The system validates both inputs.
4. Technical skills are extracted.
5. Resume skill contexts are classified.
6. Job requirements are compared with resume evidence.
7. Skill gaps are identified and prioritized.
8. Semantic similarity highlights related resume statements.
9. A personalized learning roadmap is generated.
10. The results are displayed in the dashboard and can be exported as a PDF.

## Project Structure

```text
AI-Resume-Intelligence/
├── app.py
├── components/
│   ├── __init__.py
│   └── dashboard.py
├── data/
│   ├── skills.json
│   └── learning_resources.json
├── utils/
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   ├── skill_gap_analyzer.py
│   ├── semantic_matcher.py
│   ├── skill_priority.py
│   ├── roadmap_generator.py
│   ├── context_analyzer.py
│   ├── context_resolver.py
│   ├── context_skill_gap.py
│   ├── context_priority.py
│   ├── context_roadmap.py
│   ├── intelligence_engine.py
│   ├── input_validator.py
│   ├── visualizer.py
│   └── report_generator.py
├── tests/
├── test_dashboard.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- Python 3.12
- Git
- Internet connection for the initial AI model download

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Intelligence.git
cd AI-Resume-Intelligence
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

### Create a Virtual Environment

Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the Application

```bash
python -m streamlit run app.py
```

Open the local address shown in your terminal.

## Running Tests

```bash
python -m pytest tests/ -v
```

## Model Information

The application uses:

`sentence-transformers/all-MiniLM-L6-v2`

The model is loaded from the local cache when available. Otherwise, the application attempts to download it on the first use.

## Limitations

- Skill recognition depends on the supported vocabulary and aliases.
- Context classification uses language patterns and may misinterpret ambiguous statements.
- The project does not independently verify skill proficiency.
- Semantic similarity does not prove actual experience.
- Coverage scores are not official ATS scores.
- Scanned or image-only resumes may require OCR, which is not currently included.
- Learning recommendations depend on the curated resource database.

## Privacy

Resume contents are processed within the running application. Resume text is used during analysis and retained in Streamlit session state while the session remains active.

The semantic model runs locally after it is available. The application does not intentionally submit resume text to a hosted language-model API.

For public deployments, users should avoid uploading sensitive documents until the hosting environment and its data-handling practices have been reviewed.

## Future Improvements

- Expand the technical skill database
- Improve contextual classification using trained NLP models
- Add more job-specific learning resources
- Improve explainability of matching decisions
- Add optional OCR for scanned resumes
- Improve deployment and model-loading reliability

## Disclaimer

This application is an educational project intended to assist with resume analysis and learning guidance. It should not be used as the sole basis for employment decisions.
```
