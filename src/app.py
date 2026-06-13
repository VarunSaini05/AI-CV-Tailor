import streamlit as st
from parser import ExperienceGraph
from ats_score import ATSScorer
from taylor import CVTailor
from resume_builder import ResumeBuilder
from content_generator import ContentGenerator
from pdf_generator import PDFGenerator
from pathlib import Path


st.set_page_config(page_title="AI CV Tailor", layout="centered")

# Minimal dark-mode friendly styling
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #e6edf3; }
    .stButton>button { background-color:#1f6feb; color: white; }
    textarea { background-color: #0b1220; color: #e6edf3; }
    .css-1d391kg p { color: #e6edf3; }
    .block-container { padding: 2rem 3rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def run_pipeline(job_description: str):
    graph = ExperienceGraph()
    ats = ATSScorer(graph)
    tailor = CVTailor(graph, ats)
    builder = ResumeBuilder()
    generator = ContentGenerator()
    pdfgen = PDFGenerator()

    # Build tailoring context
    context = tailor.build_context(job_description)

    # Build resume object
    resume = builder.build_resume_object(context)

    # Generate content package
    content = generator.build_content_package(resume)

    # Generate PDF and return path
    pdf_path = pdfgen.generate_pdf(content)

    return context, resume, content, pdf_path


def main():

    st.title("AI CV Tailor")
    st.subheader("ATS-Optimized Resume Generation System")

    st.write("Paste the job description below and click Generate Tailored CV.")

    job_description = st.text_area(
        "Job Description",
        value="",
        height=300,
        placeholder="Paste the full job description here...",
    )

    if st.button("Generate Tailored CV"):

        if not job_description or not job_description.strip():
            st.warning("Please paste a job description before generating the CV.")
            return

        with st.spinner("Generating tailored CV — running ATS and building PDF..."):
            try:
                context, resume, content, pdf_path = run_pipeline(job_description)

            except Exception as exc:
                st.error(f"An error occurred during generation: {exc}")
                return

        # Status messages
        st.success(f"ATS Score: {context.get('ats_score', 'N/A')}%")
        st.info(f"Detected Role Type: {context.get('role_type', 'unknown')}" )

        matched = context.get("matched_keywords", [])
        if matched:
            st.info(f"Matched Keywords: {', '.join(matched)}")
        else:
            st.warning("No matched keywords detected.")

        experiences = context.get("matched_experiences", [])
        if experiences:
            st.info("Top Experiences Selected:")
            for exp in experiences[:6]:
                st.write(f"- {exp}")
        else:
            st.warning("No experiences selected by the tailoring engine.")

        # PDF download
        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.success("PDF generated successfully.")

            st.download_button(
                label="Download Tailored PDF",
                data=pdf_bytes,
                file_name=Path(pdf_path).name,
                mime="application/pdf",
            )

        except Exception as exc:
            st.error(f"Failed to load generated PDF for download: {exc}")


if __name__ == "__main__":
    main()
