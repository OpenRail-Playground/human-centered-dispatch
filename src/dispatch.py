from pyscipopt import Model, quicksum

from dataclasses import dataclass


@dataclass
class Schicht:
    id: str
    bedarfe: dict[str, int]  # maps bedarf type to required amount
    zeitslot: int
    baustelle: str


@dataclass
class Resource:
    id: str
    hard_skills: list[str]  # list of skills this resource has to satisfy bedarfe
    extern: bool = False  # whether this resource is an external contractor

    def kosten(self) -> int:
        skill_costs = len(self.hard_skills)
        if self.extern:
            # External contractors have a higher cost and we want to assure that we always take internals first
            skill_costs *= 20
        return skill_costs

    def deckt_bedarf(self, bedarf: str) -> int:
        return 1 if bedarf in self.hard_skills else 0


def solve_dispatch(
    resourcen: list[Resource],
    schichten: list[Schicht],
    bedarfe: list[str],
    baustellen: list[str],
    timeslots: int,
) -> None:
    model = Model("Maintanance Dispatch")
    model.setMinimize()

    # variables for resource allocation considering shifts and demands
    x = {}
    for r in resourcen:
        for s in schichten:
            for b in bedarfe:
                x[(r.id, s.id, b)] = model.addVar(
                    vtype="BINARY", name=f"x_{r.id}_{s.id}_{b}", obj=r.kosten()
                )

    # variables for penalties if shifts of BSA are not stable i.e. different resources in different shifts of same BSA
    y = {}
    for b in baustellen:
        y[b] = model.addVar(vtype="INTEGER", name=f"y_{b}", obj=1)

    for s in schichten:
        for b in bedarfe:
            # ensure that each demand is covered by exactly one resource in each shift
            print(f"{s.id=}: {s.bedarfe[b]=}")
            print(list([x[(r.id, s.id, b)] * r.deckt_bedarf(b) for r in resourcen]))
            model.addCons(
                quicksum(x[(r.id, s.id, b)] * r.deckt_bedarf(b) for r in resourcen)
                >= s.bedarfe[b]
            )

    # Ensure that each resource is only scheduled to one shift and one bedarf across all timeslots
    for r in resourcen:
        for t in range(1, timeslots + 1):
            print(f"Resource {r.id} at timeslot {t}")
            print(f"Shifts: {[s.id for s in shifts_by_timeslot(schichten, t)]}")
            model.addCons(
                quicksum(
                    x[(r.id, s.id, b)]
                    for s in shifts_by_timeslot(schichten, t)
                    for b in bedarfe
                )
                <= 1
            )

    # Ensure that each baustelle has a stable shift, i.e., the same resource is assigned across all shifts
    # TODO correct?
    for bsa in baustellen:
        model.addCons(
            quicksum(
                x[(r.id, s.id, b)]
                for r in resourcen
                for s in shifts_by_baustelle(schichten, bsa)
                for b in bedarfe
            )
            <= len(schichten) * y[bsa]
        )

    # Ensure that each resource is assigned to at most 7 shifts in any 8-day timeslot window
    for r in resourcen:
        for start_t in range(
            1, timeslots - 7 + 2
        ):  # +2 because range is exclusive at end
            if start_t % 2 == 0:
                # Skip even numbered timeslots because they are for night shifts
                continue
            window_shifts = [
                s for s in schichten if start_t <= s.zeitslot < start_t + 8
            ]
            model.addCons(
                quicksum(x[(r.id, s.id, b)] for s in window_shifts for b in bedarfe) <= 7
            )

    # Ensure that no resource is assigned to shifts in consecutive timeslots i.e. do not work too munch
    for r in resourcen:
        for t in range(1, timeslots):
            shifts_t = shifts_by_timeslot(schichten, t)
            shifts_next = shifts_by_timeslot(schichten, t + 1)
            for s1 in shifts_t:
                for s2 in shifts_next:
                    for b1 in bedarfe:
                        for b2 in bedarfe:
                            model.addCons(x[(r.id, s1.id, b1)] + x[(r.id, s2.id, b2)] <= 1)

    # Optionally, if you want to ensure that a resource is not assigned to overlapping timeslots,
    # you can group by timeslot as well:
    # for r in resourcen:
    #     for t in set(s.zeitslot for s in schichten):
    #         model.addCons(
    #             quicksum(
    #                 x[(r.id, s.id, b)]
    #                 for s in schichten if s.zeitslot == t
    #                 for b in bedarfe
    #             ) <= 1
    #         )

    
    model.optimize()

    sol = model.getBestSol()
    if model.getStatus() == "optimal" and sol is not None:
        # Group assignments by timeslot and shift/baustelle
        assignments = {}
        for (r, s, b), var in x.items():
            if sol[var] > 0.5:
                schicht = next(ss for ss in schichten if ss.id == s)
                key = (schicht.zeitslot, schicht.id, schicht.baustelle)
                if key not in assignments:
                    assignments[key] = []
                assignments[key].append((r, b))
        # Print grouped assignments
        for (timeslot, schicht_id, baustelle) in sorted(assignments.keys()):
            print(f"Timeslot {timeslot}, Shift {schicht_id} (Baustelle: {baustelle}):")
            for r, b in assignments[(timeslot, schicht_id, baustelle)]:
                print(f"  Resource {r} assigned for Bedarf/Role '{b}'")
    else:
        print("No feasible solution found.")


def shifts_by_timeslot(schichten: list[Schicht], timeslot: int) -> list[Schicht]:
    """
    Returns a list of Schicht objects that match the given timeslot.
    """
    return [s for s in schichten if s.zeitslot == timeslot]


def shifts_by_baustelle(schichten: list[Schicht], baustelle: str) -> list[Schicht]:
    """
    Returns a list of Schicht objects that match the given baustelle.
    """
    return [s for s in schichten if s.baustelle == baustelle]
