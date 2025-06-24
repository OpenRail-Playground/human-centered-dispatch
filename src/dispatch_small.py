from dispatch import solve_dispatch, Schicht, Resource

resourcen = [
    Resource(id="r1", hard_skills=["b1", "b2"]),
    Resource(id="r2", hard_skills=["b1"]),
    Resource(id="r3", hard_skills=["b2"]),
]
schichten = [
    Schicht(id="s1", bedarfe={"b1": 2, "b2": 1}, zeitslot=1, baustelle="bsa1"),
    Schicht(id="s2", bedarfe={"b1": 1, "b2": 2}, zeitslot=3, baustelle="bsa2"),
]
bedarfe = ["b1", "b2"]
baustellen = ["bsa1", "bsa2"]

zeitlots = 3

solve_dispatch(resourcen, schichten, bedarfe, baustellen, zeitlots)
