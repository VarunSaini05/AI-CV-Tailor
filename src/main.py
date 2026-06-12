from parser import ExperienceGraph

graph = ExperienceGraph()

print("\n=== ALL PROJECTS ===")
print(graph.get_all_projects())

print("\n=== SEARCH: CFD ===")
print(graph.search_by_skill("CFD"))

print("\n=== ROLE CLASSIFICATION ===")

job_description = """
Looking for an aerospace engineering graduate
with CFD, ANSYS, simulation and propulsion experience.
"""

print(graph.classify_role(job_description))
