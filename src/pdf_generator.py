from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import Table, TableStyle

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER

from reportlab.lib.styles import ParagraphStyle

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"
PROFILE_PATH = DATA_DIR / "profile.json"


class PDFGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.build_custom_styles()

        self.profile = self.load_profile()

    def load_profile(self):

        if not PROFILE_PATH.exists():
            raise FileNotFoundError(
                f"Missing profile file: {PROFILE_PATH}"
            )

        with open(PROFILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    # -----------------------------------
    # CUSTOM STYLES
    # -----------------------------------

    def build_custom_styles(self):

        self.name_style = ParagraphStyle(
            "NameStyle",
            parent=self.styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=6
        )

        self.contact_style = ParagraphStyle(
            "ContactStyle",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=11,
            alignment=TA_CENTER,
            spaceAfter=6
        )

        self.section_style = ParagraphStyle(
            "SectionStyle",
            parent=self.styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=colors.black,
            spaceBefore=6,
            spaceAfter=2
        )

        self.body_style = ParagraphStyle(
            "BodyStyle",
            parent=self.styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=11,
            spaceAfter=2
        )

        self.bullet_style = ParagraphStyle(
            "BulletStyle",
            parent=self.styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=10,
            leftIndent=12,
            firstLineIndent=-6,
            spaceAfter=1
        )

        self.subheading_style = ParagraphStyle(
            "SubheadingStyle",
            parent=self.styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=11,
            spaceBefore=1,
            spaceAfter=1
        )

        self.small_italic = ParagraphStyle(
            "SmallItalic",
            parent=self.styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=9,
            spaceAfter=1
        )

        self.project_tool_style = ParagraphStyle(
            "ProjectToolStyle",
            parent=self.styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=9,
            spaceAfter=1
        )

        self.project_description_style = ParagraphStyle(
            "ProjectDescriptionStyle",
            parent=self.styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=11,
            spaceAfter=1
        )

        self.footer_style = ParagraphStyle(
            "FooterStyle",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            alignment=TA_CENTER,
            spaceBefore=8
        )

    # -----------------------------------
    # GENERATE PDF
    # -----------------------------------

    def generate_pdf(
        self,
        content
    ):

        OUTPUT_DIR.mkdir(exist_ok=True)

        pdf_path = OUTPUT_DIR / "tailored_resume.pdf"

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=28
        )

        elements = []

        # -----------------------------------
        # HEADER
        # -----------------------------------

        name = self.profile.get("full_name", "")

        contact_components = [
            self.profile.get("location", ""),
            self.profile.get("phone", ""),
            self.profile.get("email", ""),
            self.profile.get("github", "")
        ]

        contact = " | ".join(
            [item for item in contact_components if item]
        )

        elements.append(
            Paragraph(name, self.name_style)
        )

        elements.append(
            Paragraph(contact, self.contact_style)
        )

        line = Table(
            [[""]],
            colWidths=[doc.width]
        )
        line.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0)
        ]))
        elements.append(line)
        elements.append(Spacer(1, 8))

        # -----------------------------------
        # SUMMARY
        # -----------------------------------

        elements.append(
            Paragraph("PROFESSIONAL SUMMARY", self.section_style)
        )
        elements.append(
            Paragraph(content["summary"], self.body_style)
        )
        elements.append(Spacer(1, 6))

        # -----------------------------------
        # SKILLS
        # -----------------------------------

        elements.append(
            Paragraph("TECHNICAL SKILLS & TOOLS", self.section_style)
        )

        for group in content["priority_skills"]:
            elements.append(
                Paragraph(
                    f"{group['group']}: {', '.join(group['items'])}",
                    self.body_style
                )
            )

        elements.append(Spacer(1, 4))
        elements.append(line)
        elements.append(Spacer(1, 4))

        # -----------------------------------
        # WORK HISTORY
        # -----------------------------------

        elements.append(
            Paragraph("WORK HISTORY", self.section_style)
        )

        for item in content["work_history"]:
            title = item["title"]
            company_line = item["company"]
            if item.get("location"):
                company_line = f"{company_line} | {item['location']}"

            elements.append(
                Paragraph(title, self.subheading_style)
            )
            elements.append(
                Paragraph(company_line, self.body_style)
            )

            company_key = f"{title}|{item['company']}"
            bullet_list = content["work_history_bullets"].get(company_key, [])
            for bullet in bullet_list[:3]:
                elements.append(
                    Paragraph(f"• {bullet}", self.bullet_style)
                )

            elements.append(Spacer(1, 3))

        # -----------------------------------
        # PROJECTS
        # -----------------------------------

        if content.get("projects"):
            elements.append(
                Paragraph("PROJECTS", self.section_style)
            )

            for project in content["projects"]:
                elements.append(
                    Paragraph(project["title"], self.subheading_style)
                )
                if project.get("description"):
                    elements.append(
                        Paragraph(project["description"], self.project_description_style)
                    )
                elements.append(
                    Paragraph(project["tools"], self.project_tool_style)
                )
                elements.append(Spacer(1, 1))

            elements.append(Spacer(1, 5))

        # -----------------------------------
        # EDUCATION
        # -----------------------------------

        elements.append(
            Paragraph("EDUCATION", self.section_style)
        )

        for edu in content["education"]:
            degree_text = edu["degree"]
            modules_text = ", ".join(edu["modules"]) if edu["modules"] else ""
            institution_text = edu["institution"]

            elements.append(
                Paragraph(degree_text, self.subheading_style)
            )
            if modules_text:
                elements.append(
                    Paragraph(f"{modules_text}", self.small_italic)
                )
            elements.append(
                Paragraph(institution_text, self.body_style)
            )
            elements.append(Spacer(1, 1))

        # -----------------------------------
        # CERTIFICATIONS
        # -----------------------------------

        elements.append(
            Paragraph("CERTIFICATIONS", self.section_style)
        )

        for cert in content["certifications"]:
            elements.append(
                Paragraph(f"• {cert}", self.body_style)
            )

        elements.append(Spacer(1, 10))

        # -----------------------------------
        # MEMBERSHIPS
        # -----------------------------------

        elements.append(
            Paragraph("PROFESSIONAL MEMBERSHIPS", self.section_style)
        )

        memberships_text = ", ".join(content["memberships"])
        elements.append(
            Paragraph(memberships_text, self.body_style)
        )

        elements.append(Spacer(1, 10))

        # -----------------------------------
        # LANGUAGES
        # -----------------------------------

        elements.append(
            Paragraph("LANGUAGES", self.section_style)
        )

        languages_text = ", ".join(content["languages"])
        elements.append(
            Paragraph(languages_text, self.body_style)
        )

        elements.append(Spacer(1, 12))

        # -----------------------------------
        # FOOTER
        # -----------------------------------

        elements.append(
            Paragraph(content["footer"], self.contact_style)
        )

        # -----------------------------------
        # BUILD PDF
        # -----------------------------------

        doc.build(elements)

        return pdf_path
