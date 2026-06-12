from parser import ExperienceGraph
from ats_score import ATSScorer

graph = ExperienceGraph()
ats = ATSScorer(graph)

job_description = """
We are seeking an Aerospace Engineering graduate with
experience in CFD, ANSYS, SolidWorks, simulation,
technical documentation and manufacturing workflows.

Knowledge of Python automation and data analysis
is highly desirable.
"""

print("\n=== ROLE CLASSIFICATION ===")
print(graph.classify_role(job_description))

print("\n=== ATS ANALYSIS ===")
results = ats.calculate_score(job_description)

print(f"\nATS SCORE: {results['ats_score']}%")

print("\nMATCHED KEYWORDS:")
print(results["matched_keywords"])

print("\nMISSING KEYWORDS:")
print(results["missing_keywords"])

print("\nMATCHED EXPERIENCES:")
for item in results["matched_experiences"]:
    print(f"- {item.get('title', item.get('role', 'Unknown'))}")

