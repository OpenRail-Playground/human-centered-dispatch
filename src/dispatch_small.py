from dispatch import solve_dispatch, Schicht, Resource

resourcen = [
    Resource(id="Max", hard_skills=["Gleismonteur/in", "Sicherheitschef/in"]),
    Resource(id="Lisa", hard_skills=["Gleismonteur/in"]),
    Resource(id="Alex", hard_skills=["Sicherheitschef/in"]),
]
schichten = [
    Schicht(id="s1", bedarfe={"Gleismonteur/in": 2, "Sicherheitschef/in": 1}, zeitslot=1, baustelle="Zürich"),
    Schicht(id="s2", bedarfe={"Gleismonteur/in": 1, "Sicherheitschef/in": 1}, zeitslot=3, baustelle="Flughafen"),
]
bedarfe = ["Gleismonteur/in", "Sicherheitschef/in"]
baustellen = ["Zürich", "Flughafen"]

zeitlots = 3

solve_dispatch(resourcen, schichten, bedarfe, baustellen, zeitlots)
