import re

class ATSScorer:

    def __init__(self, experience_graph):
        self.graph = experience_graph

    # -----------------------------------
    # CLEAN TEXT
    # -----------------------------------

    def clean_text(self, text):

        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

        return text

    # -----------------------------------
    # EXTRACT KEYWORDS
    # -----------------------------------

    def extract_keywords(self, job_description):

        jd = self.clean_text(job_description)

        important_keywords = [
            "python",
            "solidworks",
            "ansys",
            "cfd",
            "fea",
            "cad",
            "simulation",
            "manufacturing",
            "machine learning",
            "nlp",
            "computer vision",
            "inventory",
            "excel",
            "automation",
            "api",
            "matlab",
            "technical documentation",
            "engineering",
            "operations",
            "business central",
            "data analysis"
        ]

        matched_keywords = []

        for keyword in important_keywords:

            if keyword.lower() in jd:
                matched_keywords.append(keyword)

        return list(set(matched_keywords))

    # -----------------------------------
    # ATS SCORE CALCULATION
    # -----------------------------------

    def calculate_score(self, job_description):

        keywords = self.extract_keywords(job_description)

        matched_experiences = []
        matched_keywords = []

        for keyword in keywords:

            skill_matches = self.graph.search_by_skill(keyword)
            keyword_matches = self.graph.search_by_keyword(keyword)

            combined = skill_matches + keyword_matches

            if combined:
                matched_keywords.append(keyword)

                for item in combined:
                    if item not in matched_experiences:
                        matched_experiences.append(item)

        total_keywords = len(keywords)

        if total_keywords == 0:
            score = 0
        else:
            score = int((len(matched_keywords) / total_keywords) * 100)

        missing_keywords = [
            keyword for keyword in keywords
            if keyword not in matched_keywords
        ]

        return {
            "ats_score": score,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "matched_experiences": matched_experiences
        }