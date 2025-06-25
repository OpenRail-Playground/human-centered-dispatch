import random
from dispatch import solve_dispatch, Schicht, Resource

random.seed(42)

# Hard skill pool and their target distribution (percentages)
hard_skills = [
    ("Gleismonteur/in", 0.70),
    ("Vorarbeiter/in", 0.30),
    ("Sicherheitschef/in", 0.15),
    ("TFF", 0.10),
    # ("Signaltechniker/in", 0.12),
    # ("Bauleiter/in", 0.08),
    # ("Elektriker/in", 0.10),
    # ("Fahrdienstleiter/in", 0.05),
]
hard_skill_names = [name for name, _ in hard_skills]

num_resources = 150
num_shifts = 500
num_baustellen = 50
num_timeslots = 60

# Calculate number of resources per skill
skill_counts = {name: int(frac * num_resources) for name, frac in hard_skills}

# Assign skills to resources
resources = []
for i in range(num_resources):
    skills = set()
    # Assign skills according to distribution, allow overlap
    for name, frac in hard_skills:
        if random.random() < frac:
            skills.add(name)
    # Ensure at least one skill
    if not skills:
        skills.add(random.choice(hard_skill_names))
    # About 20% extern
    extern = random.random() < 0.2
    # Frei_zeitslots: 8 on average, bundled
    num_bundles = random.randint(1, 3)
    frei_zeitslots = []
    # for _ in range(num_bundles):
    #     start = random.randint(1, num_timeslots - 5)
    #     length = random.randint(2, 6)
    #     frei_zeitslots.extend(range(start, min(start + length, num_timeslots + 1)))
    # Remove duplicates and sort
    frei_zeitslots = sorted(set(frei_zeitslots))
    if random.random() < 0.1:
        frei_zeitslots = None  # Some resources always available
    resources.append(
        Resource(
            id=f"R{i+1}",
            hard_skills=list(skills),
            extern=extern,
            frei_zeitslots=frei_zeitslots,
        )
    )

# Create baustellen
baustellen = [f"B{i+1}" for i in range(num_baustellen)]

# Assign baustellen to night-only or 24/7
baustelle_modes = {}
for b in baustellen:
    baustelle_modes[b] = "night" if random.random() < 0.4 else "all"

# Create shifts
shifts = []
for i in range(num_shifts):
    baustelle = random.choice(baustellen)
    mode = baustelle_modes[baustelle]
    # Assign timeslot
    if mode == "night":
        zeitslot = random.choice([t for t in range(2, num_timeslots + 1, 2)])
    else:
        # zeitslot = random.randint(1, num_timeslots)
        zeitslot = random.choice([t for t in range(1, num_timeslots + 1, 2)])
    # Bedarf sum 2-15, distributed by skill distribution
    total_bedarf = random.randint(2, 12)
    bedarfe = {}
    # Weighted random distribution of bedarfe
    weights = [frac for _, frac in hard_skills]
    skill_choices = random.choices(hard_skill_names, weights=weights, k=total_bedarf)
    for skill in skill_choices:
        bedarfe[skill] = bedarfe.get(skill, 0) + 1
    shifts.append(
        Schicht(
            id=f"S{i+1}",
            bedarfe=bedarfe,
            zeitslot=zeitslot,
            baustelle=baustelle,
        )
    )

# Collect all skills and baustellen used
all_bedarfe = sorted({skill for schicht in shifts for skill in schicht.bedarfe})
all_baustellen = sorted({schicht.baustelle for schicht in shifts})

print(f"Resources: {'\n'.join([str(r) for r in resources])}")
print(f"Shifts: {'\n'.join([str(s) for s in shifts])}")
print(f"Generated {len(resources)} resources, {len(shifts)} shifts, {len(all_bedarfe)} skills, {len(all_baustellen)} baustellen.")

solve_dispatch(resources, shifts, all_bedarfe, all_baustellen, num_timeslots)