from dispatch import solve_dispatch, Schicht, Resource

resourcen = [
    Resource(id="Max", hard_skills=["Gleismonteur/in", "Sicherheitschef/in"]),
    Resource(id="Lisa", hard_skills=["Gleismonteur/in"]),
    Resource(id="Alex", hard_skills=["Sicherheitschef/in"]),
    Resource(id="Moritz", hard_skills=["Gleismonteur/in"]),
    Resource(id="Petra", hard_skills=["Sicherheitschef/in"]),
    Resource(id="Moritz (ext)", hard_skills=["TFF"], extern=True),
    Resource(id="Petra (ext)", hard_skills=["Vorarbeiter/in"], extern=True),
    Resource(id="Urs", hard_skills=["TFF", "Vorarbeiter/in"]),
    Resource(id="Gisela", hard_skills=["Vorarbeiter/in", "TFF"]),
]
schichten = [
    Schicht(id="ID1", bedarfe={"Gleismonteur/in": 2, "Sicherheitschef/in": 1, "TFF": 1, "Vorarbeiter/in": 1}, zeitslot=1, baustelle="Zürich"),
    Schicht(id="ID2", bedarfe={"Gleismonteur/in": 1, "Sicherheitschef/in": 1, "TFF": 1, "Vorarbeiter/in": 1}, zeitslot=3, baustelle="Flughafen"),
    Schicht(id="ID3", bedarfe={"Gleismonteur/in": 1, "Sicherheitschef/in": 1, "TFF": 1, "Vorarbeiter/in": 1}, zeitslot=3, baustelle="Zürich"),
]
bedarfe = ["Gleismonteur/in", "Sicherheitschef/in", "TFF", "Vorarbeiter/in"]
baustellen = ["Zürich", "Flughafen"]

zeitlots = 3

solve_dispatch(resourcen, schichten, bedarfe, baustellen, zeitlots)
