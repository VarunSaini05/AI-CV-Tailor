import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class ResumeBuilder:

    def __init__(self):

        self.schema = self.load_schema()

    # -----------------------------------
    # LOAD SCHEMA
    # -----------------------------------

    def load_schema(self):

        schema_path = DATA_DIR / "resume_schema.json"

        with open(schema_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # -----------------------------------
    # BUILD STRUCTURED RESUME OBJECT
    # -----------------------------------

    def build_resume_object(
        self,
        tailoring_context
    ):

        resume_object = {

            "target_role": tailoring_context["role_type"],

            "ats_score": tailoring_context["ats_score"],

            "summary_strategy":
                tailoring_context["tailoring_strategy"],

            "matched_keywords":
                tailoring_context["matched_keywords"],

            "highlighted_experiences":
                tailoring_context["matched_experiences"],

            "missing_keywords":
                tailoring_context["missing_keywords"],

            "formatting_rules":
                self.schema
        }

        return resume_object

    # -----------------------------------
    # PRETTY DISPLAY
    # -----------------------------------

    def display_resume_blueprint(
        self,
        resume_object
    ):

        print("\n=== RESUME BLUEPRINT ===\n")

        print(f"TARGET ROLE: {resume_object['target_role']}")

        print(f"\nATS SCORE: {resume_object['ats_score']}%")

        print("\nSUMMARY STRATEGY:")
        print(resume_object["summary_strategy"])

        print("\nMATCHED KEYWORDS:")
        print(", ".join(resume_object["matched_keywords"]))

        print("\nHIGHLIGHTED EXPERIENCES:")

        for exp in resume_object["highlighted_experiences"]:
            print(f"- {exp}")

        print("\nFORMATTING RULES LOADED:")
        print("Deterministic formatting system active.")