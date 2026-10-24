
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)


def generate_pdf_report(analysis, priorities, roadmap):
    """
    Generate a context-aware resume intelligence PDF.

    Compatible with both the original and
    context-aware analysis dictionaries.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="CustomReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17346C"),
        spaceAfter=16
    ))

    styles.add(ParagraphStyle(
        name="CustomSection",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1D4ED8"),
        spaceBefore=15,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="CustomBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=6
    ))

    story = []

    def heading(value):
        story.append(
            Paragraph(value, styles["CustomSection"])
        )

    def body(value):
        story.append(
            Paragraph(
                escape(str(value)),
                styles["CustomBody"]
            )
        )

    def skill_list(values):
        return ", ".join(values) if values else "None detected"

    # ======================================
    # REPORT TITLE
    # ======================================

    story.append(Paragraph(
        "AI Resume Intelligence Report",
        styles["CustomReportTitle"]
    ))

    body(
        "Generated: "
        + datetime.now().strftime("%d %B %Y, %I:%M %p")
    )

    body(
        "A contextual comparison of skills mentioned "
        "in a resume against technical job requirements."
    )

    story.append(Spacer(1, 12))

    # ======================================
    # 1. ANALYSIS SUMMARY
    # ======================================

    heading("1. Analysis Summary")

    score = analysis.get("match_score")

    score_text = (
        f"{score:.1f}%"
        if score is not None
        else "Not available"
    )

    summary = [
        ["Metric", "Result"],
        ["Context-Aware Skill Coverage", score_text],
        [
            "Matched Job Skills",
            str(len(analysis.get("matched_skills", [])))
        ],
        [
            "Skills Requiring Attention",
            str(len(analysis.get("missing_skills", [])))
        ],
        [
            "Additional Resume Skills",
            str(len(analysis.get("additional_skills", [])))
        ]
    ]

    table = Table(
        summary,
        colWidths=[270, 220]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#17346C")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#F1F5F9")
        ]),
        ("GRID", (0, 0), (-1, -1),
         0.4, colors.HexColor("#CBD5E1")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(table)

    # ======================================
    # 2. SKILL COVERAGE
    # ======================================

    heading("2. Matched Job Skills")
    body(skill_list(analysis.get("matched_skills", [])))

    heading("3. Skills Requiring Attention")
    body(skill_list(analysis.get("missing_skills", [])))

    heading("4. Additional Resume Skills")
    body(skill_list(analysis.get("additional_skills", [])))

    # ======================================
    # 5. CONTEXT CLASSIFICATIONS
    # ======================================

    heading("5. Resume Skill Context")

    context_groups = [
        ("Currently Learning", "learning_skills"),
        ("Interested", "interested_skills"),
        ("No Experience Stated", "negated_skills"),
        ("Conflicting Evidence", "conflicting_skills"),
        ("Not Mentioned", "unmentioned_skills")
    ]

    has_context = any(
        key in analysis
        for _, key in context_groups
    )

    if has_context:
        for label, key in context_groups:
            body(
                f"{label}: "
                + skill_list(analysis.get(key, []))
            )
    else:
        body(
            "Detailed skill context is not available "
            "for this analysis."
        )

    # ======================================
    # 6. SKILL PRIORITIES
    # ======================================

    heading("6. Skill Gap Priorities")

    if priorities:
        for item in priorities:
            context = item.get("context", "unclassified")

            body(
                f"{item['skill']} - "
                f"{item['priority']} Priority "
                f"({item['category']}); "
                f"Resume context: {context}"
            )
    else:
        body("No missing recognized skills detected.")

    # ======================================
    # 7. PERSONALIZED ROADMAP
    # ======================================

    heading("7. Personalized Learning Roadmap")

    if roadmap:

        for item in roadmap:

            elements = [
                Paragraph(
                    escape(
                        f"Step {item['step']}: "
                        f"{item['skill']} "
                        f"({item['priority']} Priority)"
                    ),
                    styles["Heading3"]
                )
            ]

            if item.get("status"):
                elements.append(Paragraph(
                    "<b>Current Status:</b> "
                    + escape(item["status"]),
                    styles["CustomBody"]
                ))

            if item.get("action"):
                elements.append(Paragraph(
                    "<b>Recommended Action:</b> "
                    + escape(item["action"]),
                    styles["CustomBody"]
                ))

            if item.get("guidance"):
                elements.append(Paragraph(
                    "<b>Guidance:</b> "
                    + escape(item["guidance"]),
                    styles["CustomBody"]
                ))

            for topic in item.get("topics", []):
                elements.append(Paragraph(
                    "- " + escape(topic),
                    styles["CustomBody"]
                ))

            elements.append(Paragraph(
                "<b>Practice Project:</b> "
                + escape(item.get("project", "Not specified")),
                styles["CustomBody"]
            ))

            if item.get("resource"):
                elements.append(Paragraph(
                    "<b>Learning Resource:</b> "
                    + escape(item["resource"]),
                    styles["CustomBody"]
                ))

            elements.append(Spacer(1, 10))

            story.append(KeepTogether(elements))

    else:
        body("No learning gaps identified.")

    # ======================================
    # 8. DISCLAIMER
    # ======================================

    heading("8. Interpretation and Limitations")

    body(
        "This report uses rule-based context classification "
        "and detected skill mentions. It does not verify "
        "proficiency, represent an official ATS score, "
        "or predict hiring outcomes. Skills requiring "
        "attention may be absent from the resume rather "
        "than absent from the candidate's knowledge."
    )

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
