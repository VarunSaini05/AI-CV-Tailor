from parser import ExperienceGraph
from ats_score import ATSScorer
from taylor import CVTailor
from resume_builder import ResumeBuilder
from content_generator import ContentGenerator
from pdf_generator import PDFGenerator

from pathlib import Path


# -----------------------------------
# PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

JOB_DESCRIPTION_PATH = (
    BASE_DIR /
    "data" /
    "job_description.txt"
)

# -----------------------------------
# LOAD JOB DESCRIPTION
# -----------------------------------

with open(
    JOB_DESCRIPTION_PATH,
    "r",
    encoding="utf-8"
) as file:

    job_description = file.read()

# -----------------------------------
# INITIALIZE SYSTEMS
# -----------------------------------

graph = ExperienceGraph()

ats = ATSScorer(graph)

tailor = CVTailor(
    graph,
    ats
)

builder = ResumeBuilder()

generator = ContentGenerator()

pdf = PDFGenerator()

# -----------------------------------
# BUILD CONTEXT
# -----------------------------------

context = tailor.build_context(
    job_description
)

# -----------------------------------
# BUILD RESUME
# -----------------------------------

resume = builder.build_resume_object(
    context
)

# -----------------------------------
# GENERATE CONTENT
# -----------------------------------

content = generator.build_content_package(
    resume
)

generator.display_content_package(
    content
)

# -----------------------------------
# GENERATE PDF
# -----------------------------------

pdf_path = pdf.generate_pdf(
    content
)

# -----------------------------------
# OUTPUT
# -----------------------------------

print("\n=== PDF GENERATED ===\n")

print(f"Saved to: {pdf_path}")