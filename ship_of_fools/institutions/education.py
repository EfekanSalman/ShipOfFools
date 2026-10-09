"""TASK-206: education — a child's cognitive development gets a boost from
two sources: a small baseline ("raised by the village" / informal learning,
always present) and an institutional boost that scales with the Leadership
institution's TRUE legitimacy (a functioning institution can support actual
schooling; without one, children only get the informal baseline).

Deliberately narrow: this does NOT model literacy, curricula, or teachers as
separate agents — just a personality drift rate for conscientiousness and
openness, the two traits doc 1's own framing ties most directly to
"education" (self-discipline, curiosity about the world).
"""


def apply_schooling(child, true_legitimacy: float, informal_rate: float,
                     institutional_rate_at_full_legitimacy: float):
    """Nudge a child's conscientiousness/openness upward. No-op for adults —
    call this only for agents below adulthood_age."""
    rate = informal_rate + institutional_rate_at_full_legitimacy * true_legitimacy
    child.personality.conscientiousness = min(1.0, child.personality.conscientiousness + rate)
    child.personality.openness = min(1.0, child.personality.openness + rate * 0.5)
