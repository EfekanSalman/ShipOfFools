"""Global simulation configuration — a single source of truth for tunable parameters.

Every "experiment" in this project is just an override of one or more of these
values (see experiments/runner.py).
"""
from dataclasses import dataclass


@dataclass
class Config:
    n_agents: int = 80
    n_ticks: int = 500
    seed: int = 42
    agent_update_order: str = "fixed"  # fixed ID order or shuffled once per tick
    agent_rng_mode: str = "shared"  # shared legacy stream or independent per-agent streams

    # Environment / economy — stocks and capacity are expressed PER FOUNDER
    # and scaled by n_agents at Ship construction time. This preserves units as
    # founder population changes; it does not guarantee a calibrated scarcity
    # regime. Do not convert these to flat totals without updating Ship.__init__.
    initial_food_per_agent: float = 50.0
    initial_water_per_agent: float = 50.0
    food_regen_rate: float = 0.016       # fraction of capacity regenerated per tick
    water_regen_rate: float = 0.016
    resource_capacity_per_agent: float = 75.0
    forage_base_amount: float = 5.0      # per-kind amount a forage action can yield (before conscientiousness bonus)

    # Cognition / information (Level 3: how agents perceive & believe)
    perception_noise: float = 0.15       # noise in an agent's read of the true world state
    confirmation_bias: float = 0.6       # weight given to prior belief vs new evidence (0-1)
    misinformation_rate: float = 0.05    # probability a transmitted belief gets distorted
    # Direct scarcity-belief terms in the share/steal action scores (ISSUE-013).
    # Defaults reproduce the original hard-coded coefficients.
    steal_scarcity_weight: float = 0.9   # added to the steal score per unit scarcity_belief
    share_scarcity_weight: float = 0.5   # subtracted from the share score per unit scarcity_belief
    action_scarcity_reference: float | None = None  # if set, share/steal scores read this constant instead of the agent's belief

    # Alternative decision architecture (ISSUE-014). "heuristic" is the original
    # scoring. In "need_based", wealth is a private stock of provisions that can
    # be eaten, and forage/steal/share are scored by what they do for the
    # agent's own needs instead of by a direct scarcity-belief coefficient.
    # The provision_* fields are only read when provisions are edible.
    decision_architecture: str = "heuristic"
    # The two parts of "need_based" can be switched separately for factorial
    # runs. None follows decision_architecture (both on in "need_based", both
    # off in "heuristic").
    provisions_edible: bool | None = None    # hungry agents eat from their wealth
    need_based_scoring: bool | None = None   # forage/steal/share scored by urgency x payoff
    provision_need_per_wealth: float = 0.1  # food and water restored per unit wealth eaten (the rate the child-share rule already uses)
    provision_eat_threshold: float = 0.4    # an agent eats from its wealth when a need is below this (where scarcity stress starts)
    provision_max_per_tick: float = 1.0     # most wealth an agent can eat in one tick

    # Social (Level 4-5: relationships, trust)
    relationship_decay: float = 0.004
    trust_learning_rate: float = 0.15
    neighbor_k: int = 6                  # avg number of stable social ties per agent (TASK-101)
    rewire_prob: float = 0.1             # small-world rewiring probability
    long_range_interaction_prob: float = 0.15  # chance an interaction skips local ties (rumor spread, weak ties)

    # Institutions (Level 6: leadership emergence + basic redistribution — TASK-201/202/203)
    leadership_emergence_threshold: float = 0.012  # min avg incoming-trust-per-capita to become leader
    leadership_check_interval: int = 20           # ticks between leadership re-evaluation
    tax_rate_base: float = 0.15                   # max share of forage income taxed, at legitimacy=1
    redistribution_interval: int = 25             # ticks between equal redistribution of the public reserve
    institution_trust_noise: float = 0.2           # per-agent noise when perceiving institutional legitimacy
    reconciliation_bonus: float = 0.35   # extra trust-nudge target when repairing an already-damaged relationship

    # Culture (Level 7: emergent norms — TASK-301)
    norm_adapt_rate: float = 0.03        # how fast the population "helping norm" tracks recent behavior
    identity_feedback_strength: float = 0.3  # how strongly a formed identity reinforces its own behavior (TASK-302)

    # Metacognition (Level 1-3: introspection — TASK-601)
    self_correction_strength: float = 0.3  # how strongly conscientious agents act on their own self-read

    # Population / lifecycle (Level 2/8: generations — TASK-401/402)
    ticks_per_year: int = 15             # how many ticks make up one "year" of age
    founder_min_age: int = 18            # initial population is not a single-age cohort
    founder_max_age: int = 50
    adulthood_age: int = 16
    elderly_age: int = 60
    senescence_mortality_rate: float = 0.0015   # base per-tick death risk once elderly, grows with age
    min_reproduction_age: int = 18
    max_reproduction_age: int = 45
    birth_rate_base: float = 0.008       # per-tick chance check for each eligible mother
    reproduction_need_threshold: float = 0.5    # mother's food/water must be above this
    reproduction_max_stress: float = 0.6        # mother's stress must be below this
    birth_wealth_cost: float = 3.0
    max_population_multiplier: float = 1.8      # carrying-capacity safety valve, relative to n_agents

    # Institutions: courts/police (TASK-205), education (TASK-206)
    catch_probability_at_full_legitimacy: float = 0.6
    punishment_wealth_fraction: float = 0.5
    deterrence_strength: float = 0.5        # how strongly an agent's OWN institution_trust belief deters steal
    informal_learning_rate: float = 0.0008  # baseline child development, always active
    institutional_learning_rate: float = 0.004  # extra boost, scaled by TRUE legitimacy

    # Institutions: healthcare (TASK-207), media (TASK-208 partial)
    baseline_health_recovery_rate: float = 0.005
    institutional_health_bonus: float = 0.015     # extra recovery at full legitimacy
    media_broadcast_interval: int = 10            # ticks between leader broadcasts
    media_reach_fraction: float = 0.5             # fraction of population reachable at full legitimacy

    # Economy: learning-by-doing specialization
    forage_skill_gain: float = 0.01     # forage_skill increase per forage action
    forage_skill_bonus_max: float = 4.0  # max extra yield per kind at forage_skill=1.0

    # Psychology / physiology (Level 1-2: needs, stress)
    need_decay: float = 0.03
    stress_from_scarcity_gain: float = 0.08
    stress_recovery: float = 0.02
