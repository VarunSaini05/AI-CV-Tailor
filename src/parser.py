import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

class ExperienceGraph:

    def __init__(self):
        self.experiences = self.load_json("experiences.json")
        self.projects = self.load_json("projects.json")
        self.skills = self.load_json("skills.json")
        self.certifications = self.load_json("certifications.json")

    def load_json(self, filename):

        filepath = DATA_DIR / filename

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"[ERROR] Missing file: {filename}")
            return []

        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {filename}")
            return []

    # -----------------------------
    # EXPERIENCE RETRIEVAL
    # -----------------------------

    def get_all_experiences(self):
        return self.experiences

    def get_all_projects(self):
        return self.projects

    def get_all_certifications(self):
        return self.certifications

    # -----------------------------
    # SEARCH BY DOMAIN
    # -----------------------------

    def search_by_domain(self, domain):

        results = []

        for item in self.experiences + self.projects:

            item_domains = item.get("domains", [])

            if domain.lower() in [d.lower() for d in item_domains]:
                results.append(item)

        return results

    # -----------------------------
    # SEARCH BY SKILL
    # -----------------------------

    def search_by_skill(self, skill):

        results = []

        for item in self.experiences + self.projects:

            item_skills = item.get("skills", [])

            for s in item_skills:
                if skill.lower() in s.lower():
                    results.append(item)
                    break

        return results

    # -----------------------------
    # ATS KEYWORD MATCHING
    # -----------------------------

    def search_by_keyword(self, keyword):

        results = []

        for item in self.experiences + self.projects:

            ats_keywords = item.get("ats_keywords", [])

            if keyword.lower() in [k.lower() for k in ats_keywords]:
                results.append(item)

        return results

    # -----------------------------
    # ROLE CLASSIFIER
    # -----------------------------

    def classify_role(self, job_description):

        jd = job_description.lower()

        aerospace_keywords = [
            "cfd",
            "ansys",
            "propulsion",
            "simulation",
            "fluid",
            "aerospace"
        ]

        cad_keywords = [
            "solidworks",
            "autocad",
            "cad",
            "drafting",
            "manufacturing"
        ]

        ai_keywords = [
            "machine learning",
            "python",
            "ai",
            "nlp",
            "computer vision"
        ]

        operations_keywords = [
            "inventory",
            "warehouse",
            "erp",
            "business central",
            "operations"
        ]

        scores = {
            "aerospace": 0,
            "cad": 0,
            "ai_data": 0,
            "operations": 0
        }

        for keyword in aerospace_keywords:
            if keyword in jd:
                scores["aerospace"] += 1

        for keyword in cad_keywords:
            if keyword in jd:
                scores["cad"] += 1

        for keyword in ai_keywords:
            if keyword in jd:
                scores["ai_data"] += 1

        for keyword in operations_keywords:
            if keyword in jd:
                scores["operations"] += 1

        best_match = max(scores, key=scores.get)

        return {
            "role_type": best_match,
            "scores": scores
        }
