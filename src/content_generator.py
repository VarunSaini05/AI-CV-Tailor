import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


class ContentGenerator:

    def __init__(self):
        self.education_data = self.load_json("education.json")
        self.memberships = self.load_json("memberships.json")
        self.certifications = self.load_json("certifications.json")
        self.profile = self.load_json("profile.json")
        self.projects = self.load_json("projects.json")
        self.work_history = self.load_json("work_history.json")

    def load_json(self, filename):

        path = DATA_DIR / filename
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    # -----------------------------------
    # GENERATE PROFESSIONAL SUMMARY
    # -----------------------------------

    def generate_summary(self, resume_object):
        role = (resume_object.get("target_role") or "").lower()
        matched = resume_object.get("matched_keywords", [])

        if role == "aerospace":
            # Emphasise aerospace / CFD / propulsion skills
            focus = [k for k in ["CFD", "ANSYS", "SolidWorks", "Propulsion", "Simulation"] if k.lower() in [m.lower() for m in matched]]
            focus_text = ", ".join(focus) if focus else "CFD, ANSYS, SolidWorks, Propulsion, Simulation"
            return (
                f"Aerospace engineering specialist with hands-on experience in {focus_text}. "
                "Proven ability in CFD simulation, propulsion component design, and engineering validation using ANSYS and SolidWorks."
            )

        if role == "cad":
            focus = [k for k in ["SolidWorks", "AutoCAD", "Manufacturing Drawings", "Technical Documentation"] if k.lower() in [m.lower() for m in matched]]
            focus_text = ", ".join(focus) if focus else "SolidWorks, AutoCAD, Manufacturing Drawings, Technical Documentation"
            return (
                f"CAD Designer experienced in {focus_text}. "
                "Expert in producing manufacturing-ready 2D/3D models, technical drawings and design revision control for production workflows."
            )

        if role == "operations":
            focus = [k for k in ["Operations", "Process Improvement", "Reporting", "Data Analysis"] if k.lower() in [m.lower() for m in matched]]
            focus_text = ", ".join(focus) if focus else "Operations, Process Improvement, Stakeholder Communication, Reporting"
            return (
                f"Operations and project coordination professional focused on {focus_text}. "
                "Skilled at optimising workflows, stakeholder communication and operational reporting to drive efficiency."
            )

        if role == "ai_data":
            focus = [k for k in ["Python", "Data Analysis", "Machine Learning", "ETL"] if k.lower() in [m.lower() for m in matched]]
            focus_text = ", ".join(focus) if focus else "Python, Data Analysis, Machine Learning, ETL"
            return (
                f"Data and analytics engineer with experience in {focus_text}. "
                "Experienced in building ETL pipelines, model validation and engineering-focused data analysis for operational insights."
            )

        # Default fallback
        return (
            "Versatile engineering professional with cross-domain experience in simulation, CAD and data-driven automation."
        )

    # -----------------------------------
    # SELECT PRIORITY SKILLS
    # -----------------------------------

    def generate_priority_skills(self, resume_object):
        role = (resume_object.get("target_role") or "").lower()

        # Base pools
        engineering = ["ANSYS Fluent", "ANSYS Mechanical", "SolidWorks", "AutoCAD", "CFD"]
        programming = ["Python", "VBA", "MATLAB"]
        data = ["Pandas", "Streamlit", "ETL Pipelines", "Data Analysis"]
        documentation = ["Technical Documentation", "Manufacturing Workflows", "Engineering Reporting"]

        if role == "aerospace":
            return [
                {"group": "Engineering", "items": ["CFD", "ANSYS Fluent", "ANSYS Mechanical", "SolidWorks", "Simulation"]},
                {"group": "Programming & Automation", "items": programming},
                {"group": "Data & Analytics", "items": data},
                {"group": "Documentation", "items": documentation}
            ]

        if role == "cad":
            return [
                {"group": "CAD & Design", "items": ["SolidWorks", "AutoCAD", "Manufacturing Drawings", "Design Revisions"]},
                {"group": "Engineering", "items": ["Technical Documentation", "Manufacturing Workflows"]},
                {"group": "Programming & Automation", "items": ["SolidWorks API", "VBA", "Python"]},
                {"group": "Data & Analytics", "items": ["ETL Pipelines", "Data Analysis"]}
            ]

        if role == "operations":
            return [
                {"group": "Operations & Systems", "items": ["Inventory Management", "Business Central", "Workflow Optimisation"]},
                {"group": "Data & Reporting", "items": ["Excel", "VBA", "Data Analysis"]},
                {"group": "Documentation", "items": ["Reporting", "Stakeholder Communication"]}
            ]

        if role == "ai_data":
            return [
                {"group": "Data & Analytics", "items": ["Python", "Pandas", "Machine Learning", "ETL"]},
                {"group": "Engineering Automation", "items": ["Automation", "Streamlit", "Model Validation"]},
                {"group": "Documentation", "items": ["Technical Documentation"]}
            ]

        # Default ordering
        return [
            {"group": "Engineering", "items": engineering},
            {"group": "Programming & Automation", "items": programming},
            {"group": "Data & Analytics", "items": data},
            {"group": "Documentation & Manufacturing", "items": documentation}
        ]

    # -----------------------------------
    # SELECT TOP EXPERIENCES
    # -----------------------------------

    def generate_experience_highlights(self, resume_object):
        experiences = resume_object.get("highlighted_experiences", [])
        return experiences[:4]

    # -----------------------------------
    # WORK HISTORY
    # -----------------------------------

    def generate_work_history(self, resume_object):
        # Reorder the canonical work history to prioritise role-relevant titles
        role = (resume_object.get("target_role") or "").lower()

        # Define ordering preferences per role (titles as in work_history.json)
        priorities = []
        if role == "aerospace":
            priorities = ["RESEARCH INTERN", "CAD DESIGNER (2D & 3D)", "LOGISTICS SUPERVISOR"]
        elif role == "cad":
            priorities = ["CAD DESIGNER (2D & 3D)", "RESEARCH INTERN", "LOGISTICS SUPERVISOR"]
        elif role == "operations":
            priorities = ["LOGISTICS SUPERVISOR", "CLASS REPRESENTATIVE", "CAD DESIGNER (2D & 3D)"]
        elif role == "ai_data":
            priorities = ["LOGISTICS SUPERVISOR", "RESEARCH INTERN", "VOLUNTEER CITIZEN SCIENTIST"]

        ordered = []
        remaining = []

        for item in self.work_history:
            title = item.get("title", "").upper()
            if title in priorities:
                ordered.append(item)
            else:
                remaining.append(item)

        # Sort ordered by the priority list order
        ordered.sort(key=lambda i: priorities.index(i.get("title", "").upper()) if i.get("title", "").upper() in priorities else 999)

        return ordered + remaining

    def generate_work_history_bullets(self, resume_object):
        # Role-aware bullets per canonical work history entry
        role = (resume_object.get("target_role") or "").lower()
        bullets = {}

        for item in self.work_history:
            title = item["title"]
            company_key = f"{title}|{item['company']}"

            # Default libraries per title with role-specific variants
            if title == "CAD DESIGNER (2D & 3D)":
                if role == "cad":
                    bullets[company_key] = [
                        "Produced manufacturing-ready SolidWorks 2D and 3D CAD models and detailed fabrication drawings.",
                        "Maintained drawing revision control and coordinated design review cycles with production teams.",
                        "Developed CAD automation scripts to speed up repetitive modelling tasks."
                    ]
                elif role == "aerospace":
                    bullets[company_key] = [
                        "Generated simulation-ready CAD geometry for aerodynamic and propulsion component analysis using SolidWorks.",
                        "Supported CAD-to-mesh workflows for CFD validation and ANSYS integration.",
                        "Produced technical documentation to enable engineering validation and manufacturing handoff."
                    ]
                elif role == "operations":
                    bullets[company_key] = [
                        "Coordinated CAD deliverables and ensured timely handover to manufacturing and logistics teams.",
                        "Managed document control for engineering drawings and supported production planning.",
                        "Implemented process improvements to streamline design-to-manufacture workflows."
                    ]
                else:
                    bullets[company_key] = [
                        "Delivered detailed SolidWorks 2D and 3D CAD models for manufacturing-ready mechanical assemblies.",
                        "Produced technical drawings, assembly documentation and build-ready fabrication specifications.",
                        "Coordinated design revisions and review cycles with engineering and production teams."
                    ]

            elif title == "LOGISTICS SUPERVISOR":
                if role == "operations":
                    bullets[company_key] = [
                        "Implemented Excel and VBA process tracking for warehouse workflows, improving inventory accuracy by automating reconciliations.",
                        "Led Business Central rollout support and trained operational users to improve ERP adoption.",
                        "Built data-driven reporting and KPIs to align logistics operations with production requirements."
                    ]
                elif role == "aerospace":
                    bullets[company_key] = [
                        "Coordinated logistics support for engineering projects, ensuring parts and materials were available for aerospace validation workflows.",
                        "Documented inventory control procedures and provided technical reporting to support manufacturing handovers.",
                        "Applied data-driven process improvements to improve supply chain reliability for production teams."
                    ]
                elif role == "cad":
                    bullets[company_key] = [
                        "Supported manufacturing planning and drawing release workflows through enhanced inventory tracking.",
                        "Produced documentation for engineering handovers and design change implementation.",
                        "Streamlined warehouse processes to reduce delays in CAD-to-production handoffs."
                    ]
                elif role == "ai_data":
                    bullets[company_key] = [
                        "Built ETL processes and data cleaning pipelines to support inventory analytics and reporting.",
                        "Developed automated dashboards and scripts to reduce manual reconciliation effort.",
                        "Provided structured datasets for machine learning and predictive analytics projects."
                    ]
                else:
                    bullets[company_key] = [
                        "Implemented Excel and VBA process tracking for warehouse workflows, improving inventory control.",
                        "Documented operational handover procedures and supported Business Central rollout.",
                        "Built data-driven reporting to align logistics operations with manufacturing support needs."
                    ]

            elif title == "RESEARCH INTERN":
                if role == "aerospace":
                    bullets[company_key] = [
                        "Performed CFD analysis using ANSYS Fluent for liquid hydrogen propulsion systems.",
                        "Conducted mesh convergence studies and thermo-structural validation workflows.",
                        "Developed MATLAB models supporting propulsion performance analysis."
                    ]
                elif role == "cad":
                    bullets[company_key] = [
                        "Produced engineering models and simulation-ready CAD geometry using SolidWorks to support analysis workflows.",
                        "Supported design validation and produced engineering documentation for manufacturing handover.",
                        "Collaborated on design revisions and manufacturing-oriented engineering analysis."
                    ]
                elif role == "operations":
                    bullets[company_key] = [
                        "Coordinated technical project activities and produced engineering reporting to support stakeholders.",
                        "Analysed simulation outputs and authored structured technical documentation for validation handovers.",
                        "Facilitated multidisciplinary collaboration across engineering and operations teams."
                    ]
                elif role == "ai_data":
                    bullets[company_key] = [
                        "Implemented data preprocessing and MATLAB scripts to clean simulation outputs for analysis.",
                        "Performed data-driven validation and contributed to model development workflows.",
                        "Developed reproducible analysis pipelines to support engineering research."
                    ]
                else:
                    bullets[company_key] = [
                        "Spearheaded CFD workflows for liquid hydrogen propulsion nozzle design using ANSYS and SolidWorks.",
                        "Validated aero-mechanics and thermodynamic performance through mesh convergence and thermal stress analysis.",
                        "Developed MATLAB models for simulation data processing and fusion propulsion DEC concept evaluation."
                    ]

            elif title == "VOLUNTEER CITIZEN SCIENTIST":
                if item["company"] == "Zooniverse":
                    if role == "ai_data":
                        bullets[company_key] = [
                            "Reviewed and labelled large astronomy datasets to produce training data for classification models.",
                            "Contributed to data quality checks and supported downstream analysis workflows.",
                            "Documented classification criteria to improve consistency across contributors."
                        ]
                    else:
                        bullets[company_key] = [
                            "Reviewed astronomy datasets to identify supernovae, black holes and deep-space anomalies."
                        ]
                else:
                    bullets[company_key] = [
                        "Contributed to environmental and climate observation workflows through scientific data collection and analysis."
                    ]

            elif title == "CLASS REPRESENTATIVE":
                if role == "operations":
                    bullets[company_key] = [
                        "Represented student engineering cohorts and coordinated academic feedback to improve program workflows.",
                        "Organised technical activities and facilitated communication between students and faculty.",
                        "Managed meeting logistics and produced concise reports for stakeholders."
                    ]
                else:
                    bullets[company_key] = [
                        "Represented student engineering cohorts, coordinated academic feedback and organised technical activities."
                    ]

            else:
                bullets[company_key] = [
                    "Delivered structured technical support, documentation and operational coordination."]

        return bullets

    # -----------------------------------
    # GENERATE EXPERIENCE BULLETS
    # -----------------------------------

    def generate_experience_bullets(self, resume_object):

        role = resume_object["target_role"]
        bullets = {}

        for exp in resume_object["highlighted_experiences"][:4]:
            if "Hydrogen" in exp:
                bullets[exp] = [
                    "Conducted CFD and thermo-structural simulations with ANSYS Fluent and ANSYS Mechanical.",
                    "Validated hydrogen nozzle performance using mesh-independence checks and high-enthalpy flow analysis.",
                    "Automated SolidWorks geometry generation and produced engineering CAD documentation."
                ]

            elif "Warehouse" in exp:
                bullets[exp] = [
                    "Processed 243000 warehouse movement records to enable inventory analytics and operational exception reporting.",
                    "Built Python ETL workflows and Streamlit dashboards for KPI monitoring and stock risk analysis.",
                    "Automated Business Central reporting to reduce manual reconciliation effort."
                ]

            elif "Logistics" in exp:
                bullets[exp] = [
                    "Supported warehouse systems, inventory investigations and Business Central rollout processes.",
                    "Delivered Excel automation tools to reduce stock reconciliation time and operational errors.",
                    "Produced technical documentation for support workflows and handover procedures."
                ]

            elif "CAD" in exp:
                bullets[exp] = [
                    "Produced manufacturing-ready technical drawings and engineering documentation for fabrication handoff.",
                    "Delivered SolidWorks and AutoCAD CAD support for production-intent design updates.",
                    "Managed drawing revisions, assembly instructions and design review outputs."
                ]

            elif "AI" in exp or "Predictive" in exp:
                bullets[exp] = [
                    "Designed predictive-maintenance workflows using NASA CMAPSS datasets for aircraft engine health analysis.",
                    "Implemented Python data preprocessing, feature engineering and model validation pipelines.",
                    "Delivered engineering-focused analytics to support asset reliability and maintenance planning."
                ]

            elif "Scientific" in exp:
                bullets[exp] = [
                    "Reviewed over 1000 astronomy dataset images as part of citizen science research initiatives.",
                    "Contributed scientific classification workflows supporting Zooniverse and NASA data analysis."
                ]

            else:
                bullets[exp] = [
                    "Delivered structured technical support with a focus on documentation, systems and process improvement."]

        return bullets

    # -----------------------------------
    # PROJECTS SECTION
    # -----------------------------------

    def generate_projects(self, resume_object):
        # Select and order projects based on target role
        role = (resume_object.get("target_role") or "").lower()

        role_project_map = {
            "aerospace": ["hydrogen_nozzle_project", "fusion_reactor_dec_system", "aircraft_preflight_ai"],
            "cad": ["hydrogen_nozzle_project", "warehouse_intelligence_platform", "ai_life_coach"],
            "operations": ["warehouse_intelligence_platform", "ai_life_coach", "aircraft_preflight_ai"],
            "ai_data": ["warehouse_intelligence_platform", "aircraft_preflight_ai", "ai_life_coach"]
        }

        preferred = role_project_map.get(role, [p["id"] for p in self.projects])[:3]

        # Role-specific descriptions per project
        project_descriptions = {
            "hydrogen_nozzle_project": {
                "aerospace": "Developed and validated a high-enthalpy hydrogen propulsion nozzle using CFD and thermo-structural ANSYS workflows, focusing on propulsion performance and simulation accuracy.",
                "cad": "Produced parametric SolidWorks models and automated geometry generation to support propulsion nozzle design and manufacturing handoff.",
                "operations": "Managed testing data collection, validation procedures and produced engineering reports to support propulsion system integration.",
                "ai_data": "Processed simulation outputs and built data pipelines for analysis and model validation in propulsion research."
            },
            "warehouse_intelligence_platform": {
                "aerospace": "Adapted inventory analytics techniques to support aerospace supply workflows and parts traceability.",
                "cad": "Integrated inventory data with CAD bill-of-materials to improve design-to-manufacture traceability.",
                "operations": "Built an inventory analytics platform processing 243000 records to enable warehouse intelligence and operational reporting.",
                "ai_data": "Implemented ETL and analytics pipelines to process 243000 warehouse movement records for predictive inventory analytics."
            },
            "aircraft_preflight_ai": {
                "aerospace": "Designed predictive-maintenance AI workflows for aircraft engine health using NASA CMAPSS datasets to support safety and reliability.",
                "cad": "Generated simulation datasets and CAD-linked test cases to validate maintenance workflows against physical assembly constraints.",
                "operations": "Developed analytics-driven maintenance reporting to prioritise preflight checks and reduce operational risk.",
                "ai_data": "Built ML pipelines and feature engineering workflows for predictive maintenance using NASA CMAPSS datasets."
            },
            "ai_life_coach": {
                "aerospace": "Applied NLP and recommendation systems for user-facing tools to support crew wellbeing and training simulations.",
                "cad": "Built supportive tools to manage design feedback and user sentiment across engineering teams.",
                "operations": "Implemented user workflow automation and reporting for coaching interactions and support metrics.",
                "ai_data": "Developed NLP pipelines and sentiment analysis models for personalised coaching recommendations."
            },
            "fusion_reactor_dec_system": {
                "aerospace": "Developed conceptual Direct Energy Conversion (DEC) models and simulation workflows using MATLAB and SolidWorks for propulsion research.",
                "cad": "Produced system-level CAD models to support integration and simulation of DEC components.",
                "operations": "Coordinated testing and validation processes for prototype DEC systems and managed documentation flows.",
                "ai_data": "Analysed simulation outputs and built diagnostic pipelines to support fusion reactor control system research."
            }
        }

        selected = []

        for pid in preferred:
            for project in self.projects:
                if project["id"] == pid:
                    tools = ", ".join(project["tools"][:5])
                    role_descs = project_descriptions.get(pid, {})
                    desc = role_descs.get(role) if isinstance(role_descs, dict) else None
                    if not desc:
                        desc = project.get("description", "") or ""
                    selected.append({
                        "title": project["title"],
                        "description": desc,
                        "tools": tools
                    })
                    break

        return selected

    # -----------------------------------
    # EDUCATION SECTION
    # -----------------------------------

    def generate_education(self):
        return self.education_data

    # -----------------------------------
    # CERTIFICATIONS SECTION
    # -----------------------------------

    def generate_certifications(self):

        exact_titles = [
            "Learning from Dark Matter and Energy",
            "Explore Space Tech: Rockets 101",
            "Technology Drives Exploration: Detecting Exoplanets",
            "Life in Space"
        ]

        return [
            f"{cert.get('issuer', '').upper()}: {cert['title']}"
            for cert in self.certifications
            if cert.get("title") in exact_titles
        ]

    # -----------------------------------
    # MEMBERSHIPS SECTION
    # -----------------------------------

    def generate_memberships(self):
        return self.memberships

    # -----------------------------------
    # LANGUAGES SECTION
    # -----------------------------------

    def generate_languages(self):
        return [
            "English (Fluent)",
            "Hindi (Native)",
            "German (Intermediate)"
        ]

    # -----------------------------------
    # FOOTER
    # -----------------------------------

    def generate_footer(self):
        return "References available on request"

    # -----------------------------------
    # BUILD CONTENT PACKAGE
    # -----------------------------------

    def build_content_package(self, resume_object):

        content = {
            "summary": self.generate_summary(resume_object),
            "priority_skills": self.generate_priority_skills(resume_object),
            "work_history": self.generate_work_history(resume_object),
            "work_history_bullets": self.generate_work_history_bullets(resume_object),
            "projects": self.generate_projects(resume_object),
            "education": self.generate_education(),
            "certifications": self.generate_certifications(),
            "memberships": self.generate_memberships(),
            "languages": self.generate_languages(),
            "footer": self.generate_footer()
        }

        return content

    # -----------------------------------
    # DISPLAY CONTENT
    # -----------------------------------

    def display_content_package(self, content):

        print("\n=== GENERATED RESUME CONTENT ===\n")

        print("PROFESSIONAL SUMMARY:\n")
        print(content["summary"])

        print("\nTECHNICAL SKILLS & TOOLS:\n")
        for group in content["priority_skills"]:
            print(f"{group['group']}: {', '.join(group['items'])}")

        print("\nWORK HISTORY / EXPERIENCE:\n")
        for item in content["work_history"]:
            location_text = f" | {item['location']}" if item.get('location') else ""
            print(f"{item['title']} | {item['company']}{location_text}")

        print("\nPROJECTS:\n")
        for project in content["projects"]:
            print(f"{project['title']}")
            print(f"{project['description']}")
            print(f"({project['tools']})")

        print("\nEDUCATION:\n")
        for edu in content["education"]:
            modules = ", ".join(edu["modules"]) if edu["modules"] else ""
            print(f"• {edu['degree']}")
            if modules:
                print(f"  ({modules})")
            print(f"  {edu['institution']}")

        print("\nCERTIFICATIONS:\n")
        for cert in content["certifications"]:
            print(f"- {cert}")

        print("\nPROFESSIONAL MEMBERSHIPS:\n")
        for membership in content["memberships"]:
            print(f"- {membership}")

        print("\nLANGUAGES:\n")
        for language in content["languages"]:
            print(f"- {language}")

        print(f"\n{content['footer']}")

