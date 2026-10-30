"""TASK-401/402: aging, death, and birth. Agents are not immortal, and a new
agent is not a blank slate — it inherits a blend of its parents' personality
("nature") and a snapshot of their current worldview ("nurture"), per doc 3's
"its genetic traits + family + culture ... shape it". A child's
IDENTITY, however, starts at None like any founder's — identity must still be
earned through the child's own lived experience (TASK-302's core rule), it is
NOT inherited.

Kept as its own module (not baked into Agent/Simulation) so the population
mechanics can be extended (education, more elaborate mate selection, ...)
without touching the rest of the tick loop.
"""
import random
from typing import Dict, List, Optional

from ..agents.agent import Agent


class Lifecycle:
    def __init__(self, config):
        self.config = config
        self.next_id: int = config.n_agents  # founders occupy ids 0..n_agents-1
        self.cumulative_births = 0
        self.cumulative_deaths_old_age = 0
        self.cumulative_deaths_starvation = 0

    def seed_founder_ages(self, agents: List[Agent], rng: random.Random):
        cfg = self.config
        for a in agents:
            a.age_years = rng.randint(cfg.founder_min_age, cfg.founder_max_age)

    def age_and_check_senescence(self, agent: Agent, rng: random.Random) -> bool:
        """Advance age by one tick; return True if the agent dies of old age now."""
        cfg = self.config
        agent.age_ticks += 1
        if agent.age_ticks % cfg.ticks_per_year == 0:
            agent.age_years += 1
        if agent.age_years >= cfg.elderly_age:
            years_elderly = agent.age_years - cfg.elderly_age
            risk = cfg.senescence_mortality_rate * (1 + 0.15 * years_elderly)
            if rng.random() < risk:
                self.cumulative_deaths_old_age += 1
                return True
        return False

    def maybe_reproduce(self, mother: Agent, candidate_fathers: List[Agent], rng: random.Random,
                         current_population: int) -> Optional[Agent]:
        cfg = self.config
        if current_population >= int(cfg.n_agents * cfg.max_population_multiplier):
            return None  # carrying-capacity safety valve
        if not (cfg.min_reproduction_age <= mother.age_years <= cfg.max_reproduction_age):
            return None
        if min(mother.needs.food, mother.needs.water) < cfg.reproduction_need_threshold:
            return None
        if mother.stress > cfg.reproduction_max_stress:
            return None
        if rng.random() >= cfg.birth_rate_base:
            return None

        # father: a trusted local tie of reproductive age (none found -> no birth this tick)
        candidates = [f for f in candidate_fathers
                      if f.alive and f.id != mother.id
                      and cfg.min_reproduction_age <= f.age_years <= cfg.max_reproduction_age]
        if not candidates:
            return None
        father = rng.choice(candidates)

        child = Agent(self.next_id, rng)
        self.next_id += 1
        child.age_ticks = 0
        child.age_years = 0
        child.parent_ids = (mother.id, father.id)

        # nature: blended personality + mutation noise, not a blank slate
        for trait in ("openness", "conscientiousness", "risk_tolerance",
                      "empathy", "dominance", "conformity", "curiosity"):
            blended = 0.5 * getattr(mother.personality, trait) + 0.5 * getattr(father.personality, trait)
            setattr(child.personality, trait, min(1.0, max(0.0, blended + rng.gauss(0, 0.08))))

        # nurture: inherits the parents' CURRENT worldview as a starting prior
        child.beliefs.scarcity_belief = 0.5 * (mother.beliefs.scarcity_belief + father.beliefs.scarcity_belief)
        child.beliefs.institution_trust = 0.5 * (mother.beliefs.institution_trust + father.beliefs.institution_trust)

        mother.wealth = max(0.0, mother.wealth - cfg.birth_wealth_cost)
        mother.children.append(child)
        father.children.append(child)
        self.cumulative_births += 1
        return child
