"""TASK-301: a social norm that EMERGES from population behavior rather than
being fixed at t=0 (doc 2, point 4). `helping_norm` is a slow-moving,
population-level "how normal is it to help each other around here" signal,
built from last tick's observed cooperation_rate — not from any individual's
belief. It then feeds back into conformity-driven agents' decisions
(cognition/decision.py), which is how a norm actually becomes self-reinforcing
or self-eroding rather than just a passive statistic.

Second dimension (multi-dimensional culture, doc 1 section 10 — only 2 of the
7 suggested abstract axes are modeled; individualism/collectivism, tradition/
change and economic preferences are NOT): `authority_norm` — "how much does
this population defer to institutional authority" — built from last tick's
population-average `institution_trust` BELIEF (not the institution's true
legitimacy), so a population can drift toward a deferential culture even
around an institution that doesn't really deserve the trust.
"""


class Norms:
    def __init__(self, adapt_rate: float = 0.03):
        self.helping_norm: float = 0.5    # 0-1, starts neutral — not assumed from tick 0
        self.authority_norm: float = 0.5  # 0 = autonomy/egalitarian, 1 = hierarchy/deference
        self.adapt_rate = adapt_rate

    def update(self, observed_cooperation_rate: float, observed_institution_trust: float):
        self.helping_norm += self.adapt_rate * (observed_cooperation_rate - self.helping_norm)
        self.helping_norm = min(1.0, max(0.0, self.helping_norm))
        self.authority_norm += self.adapt_rate * (observed_institution_trust - self.authority_norm)
        self.authority_norm = min(1.0, max(0.0, self.authority_norm))
