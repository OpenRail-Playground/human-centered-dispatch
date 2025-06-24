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
    Schicht(
        id=f"ID{zeitslot}", bedarfe={"TFF": 1}, zeitslot=zeitslot, baustelle="Zürich"
    )
    for zeitslot in range(2, 56, 2)
] + [
    Schicht(id=f"ID31", bedarfe={"TFF": 1}, zeitslot=1, baustelle="Zürich",),
    Schicht(id=f"ID32", bedarfe={"TFF": 1}, zeitslot=3, baustelle="Zürich"),
    Schicht(id=f"ID33", bedarfe={"TFF": 1}, zeitslot=5, baustelle="Zürich")
]

bedarfe = sorted({skill for schicht in schichten for skill in schicht.bedarfe})
baustellen = sorted({schicht.baustelle for schicht in schichten})

zeitlots = max(schicht.zeitslot for schicht in schichten)

solve_dispatch(resourcen, schichten, bedarfe, baustellen, zeitlots)
