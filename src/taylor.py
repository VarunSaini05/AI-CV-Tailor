class CVTailor:

    def __init__(self, graph, ats_engine):

        self.graph = graph
        self.ats = ats_engine

    # -----------------------------------
    # EXPERIENCE WEIGHTING ENGINE
    # -----------------------------------

    def rank_experiences(
        self,
        experiences,
        role_type,
        keywords
    ):

        ranked = []

        for item in experiences:

            score = 0

            title = item.get(
                "title",
                item.get("role", "")
            ).lower()

            item_domains = [
                d.lower()
                for d in item.get("domains", [])
            ]

            item_skills = [
                s.lower()
                for s in item.get("skills", [])
            ]

            ats_keywords = [
                k.lower()
                for k in item.get("ats_keywords", [])
            ]

            # -----------------------------------
            # KEYWORD MATCH SCORING
            # -----------------------------------

            for keyword in keywords:

                keyword = keyword.lower()

                if keyword in item_skills:
                    score += 5

                if keyword in ats_keywords:
                    score += 4

                if keyword in item_domains:
                    score += 3

                if keyword in title:
                    score += 6

            # -----------------------------------
            # ROLE PRIORITY WEIGHTING
            # -----------------------------------

            if role_type == "aerospace":

                aerospace_terms = [
                    "cfd",
                    "simulation",
                    "ansys",
                    "propulsion",
                    "aerospace"
                ]

                for term in aerospace_terms:

                    if (
                        term in item_skills
                        or term in ats_keywords
                        or term in item_domains
                        or term in title
                    ):
                        score += 8

            elif role_type == "cad":

                cad_terms = [
                    "solidworks",
                    "cad",
                    "manufacturing",
                    "drafting"
                ]

                for term in cad_terms:

                    if (
                        term in item_skills
                        or term in ats_keywords
                        or term in item_domains
                        or term in title
                    ):
                        score += 8

            elif role_type == "ai_data":

                ai_terms = [
                    "python",
                    "machine learning",
                    "nlp",
                    "automation",
                    "data analysis"
                ]

                for term in ai_terms:

                    if (
                        term in item_skills
                        or term in ats_keywords
                        or term in item_domains
                        or term in title
                    ):
                        score += 8

            elif role_type == "operations":

                ops_terms = [
                    "inventory",
                    "operations",
                    "workflow",
                    "systems",
                    "warehouse"
                ]

                for term in ops_terms:

                    if (
                        term in item_skills
                        or term in ats_keywords
                        or term in item_domains
                        or term in title
                    ):
                        score += 8

            ranked.append((score, item))

        ranked.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [item for score, item in ranked]

    # -----------------------------------
    # BUILD TAILORING CONTEXT
    # -----------------------------------

    def build_context(self, job_description):

        role_data = self.graph.classify_role(
            job_description
        )

        ats_results = self.ats.calculate_score(
            job_description
        )

        role_type = role_data["role_type"]

        matched_keywords = ats_results[
            "matched_keywords"
        ]

        matched_experiences = ats_results[
            "matched_experiences"
        ]

        ranked_experiences = self.rank_experiences(
            matched_experiences,
            role_type,
            matched_keywords
        )

        experience_titles = []

        for item in ranked_experiences:

            title = item.get(
                "title",
                item.get("role", "Unknown Experience")
            )

            experience_titles.append(title)

        tailoring_strategy = self.generate_strategy(
            role_type,
            matched_keywords
        )

        return {

            "role_type":
                role_type,

            "ats_score":
                ats_results["ats_score"],

            "matched_keywords":
                matched_keywords,

            "missing_keywords":
                ats_results["missing_keywords"],

            "matched_experiences":
                experience_titles,

            "tailoring_strategy":
                tailoring_strategy
        }

    # -----------------------------------
    # STRATEGY GENERATOR
    # -----------------------------------

    def generate_strategy(
        self,
        role_type,
        keywords
    ):

        if role_type == "aerospace":

            return (
                "Focus heavily on CFD, simulation, "
                "ANSYS workflows, propulsion systems, "
                "technical documentation, engineering analysis "
                "and manufacturing-oriented CAD workflows."
            )

        elif role_type == "cad":

            return (
                "Emphasize SolidWorks, technical drafting, "
                "manufacturing workflows, assemblies, "
                "fabrication support and CAD automation."
            )

        elif role_type == "ai_data":

            return (
                "Highlight Python, machine learning, "
                "data analysis, NLP, automation systems "
                "and analytical workflows."
            )

        elif role_type == "operations":

            return (
                "Prioritize workflow optimization, "
                "systems support, inventory analysis, "
                "technical troubleshooting and process improvement."
            )

        return (
            "Focus on adaptability, technical problem-solving "
            "and cross-domain engineering experience."
        )

    # -----------------------------------
    # GENERATE CLAUDE PROMPT
    # -----------------------------------

    def generate_prompt(self, job_description):

        context = self.build_context(
            job_description
        )

        prompt = f"""
You are an expert recruiter-focused CV writer.

Your task is to tailor a highly ATS-optimized,
human-readable and recruiter-friendly CV.

TARGET ROLE TYPE:
{context['role_type']}

ATS SCORE:
{context['ats_score']}%

MATCHED KEYWORDS:
{", ".join(context['matched_keywords'])}

MISSING KEYWORDS:
{", ".join(context['missing_keywords'])}

MOST RELEVANT EXPERIENCES:
{chr(10).join("- " + exp for exp in context['matched_experiences'])}

TAILORING STRATEGY:
{context['tailoring_strategy']}

JOB DESCRIPTION:
{job_description}

Instructions:
- Aggressively optimize for ATS alignment
- Keep all claims truthful
- Prioritize quantified achievements
- Emphasize recruiter-relevant terminology
- Keep formatting professional and concise
- Focus heavily on matched experiences
"""

        return prompt
