"""Main simulation engine integrating the current model subsystems.

The implemented scope and research limitations are described in ODD_D.md and
ARCHITECTURE.md. Actions are sequential and the schedule is configurable as
fixed agent-list order or a per-tick shuffled order.
"""
import random

from ..agents.agent import Agent
from ..environment.ship import Ship
from ..sociology.social_network import SocialNetwork, build_neighbor_structure
from ..information.rumors import transmit_belief
from ..cognition.decision import choose_action
from ..institutions.leadership import Leadership
from ..institutions.law_enforcement import LawEnforcement
from ..institutions.education import apply_schooling
from ..institutions.healthcare import health_recovery_rate
from ..institutions.media import broadcast as media_broadcast
from ..culture.norms import Norms
from ..population.lifecycle import Lifecycle
from ..metrics.tracker import MetricsTracker


class Simulation:
    def __init__(self, config):
        self.config = config
        if config.decision_architecture not in ("heuristic", "need_based"):
            raise ValueError("decision_architecture must be 'heuristic' or 'need_based'")
        self.need_based = config.decision_architecture == "need_based"
        # need value of one theft (at most 2.0 wealth, see _apply_action)
        # relative to one base forage, both in need units
        self.steal_relative_gain = (2.0 * config.provision_need_per_wealth) / (config.forage_base_amount / 10)
        self.rng = random.Random(config.seed)
        # Keep scheduling randomness separate so permutation draws do not
        # consume the RNG stream used by agent decisions and the environment.
        self.schedule_rng = random.Random(config.seed ^ 0x5A17C9E3)
        self.ship = Ship(config, self.rng)
        self.agents = [Agent(i, self.rng) for i in range(config.n_agents)]
        self.agent_ids = [a.id for a in self.agents]
        neighbors = build_neighbor_structure(self.agent_ids, config.neighbor_k,
                                              config.rewire_prob, self.rng)
        self.social = SocialNetwork(self.agent_ids, self.rng, neighbors=neighbors)
        self.institutions = Leadership(config.leadership_emergence_threshold,
                                        config.leadership_check_interval)
        self.law_enforcement = LawEnforcement(config.catch_probability_at_full_legitimacy,
                                               config.punishment_wealth_fraction)
        self.cumulative_thieves_caught = 0
        self.norms = Norms(config.norm_adapt_rate)
        self.lifecycle = Lifecycle(config)
        self.lifecycle.seed_founder_ages(self.agents, self.rng)  # TASK-401: not a single-age cohort
        self._configure_agent_rngs(self.agents)
        self.metrics = MetricsTracker()

    def _configure_agent_rngs(self, agents):
        """Assign stable per-agent streams when the experimental mode requests it."""
        if self.config.agent_rng_mode not in ("shared", "per_agent"):
            raise ValueError("agent_rng_mode must be 'shared' or 'per_agent'")
        if self.config.agent_rng_mode == "per_agent":
            for agent in agents:
                agent.rng = random.Random(self.config.seed ^ ((agent.id + 1) * 0x9E3779B1))

    def _action_rng(self, agent):
        return agent.rng if self.config.agent_rng_mode == "per_agent" else self.rng

    def _register_newborn(self, child, mother, father):
        """Wire a freshly-born agent into the social graph: mutual ties with
        both parents, plus a couple of the mother's existing ties (born into
        an existing community, not a stranger to it)."""
        self.social.trust[child.id] = {}
        self.social.neighbors[child.id] = set()
        for parent_id in (mother.id, father.id):
            self.social.neighbors[child.id].add(parent_id)
            self.social.neighbors[parent_id].add(child.id)
        mother_neighbors = list(self.social.neighbors.get(mother.id, ()))
        rng = self._action_rng(mother)
        for extra in rng.sample(mother_neighbors, min(2, len(mother_neighbors))):
            self.social.neighbors[child.id].add(extra)
            self.social.neighbors[extra].add(child.id)

    def _perceive_and_update_beliefs(self, agent):
        cfg = self.config
        true_scarcity = self.ship.resources.true_scarcity()
        rng = self._action_rng(agent)
        noise = rng.gauss(0, cfg.perception_noise)
        # stress adds a negativity bias: perceived scarcity skews upward when stressed.
        # ISSUE-003 fix (applied here too for consistency): don't clip the noisy
        # observation itself before blending — when true_scarcity sits near 0 or 1,
        # pre-clipping would introduce the same systematic bias fixed for
        # institution_trust below. Only the final belief is clipped.
        observed = true_scarcity + noise + 0.15 * agent.stress
        agent.beliefs.update_scarcity(observed, cfg.confirmation_bias)

        # TASK-203: institution_trust is updated from a noisy, individual read of
        # the institution's real legitimacy — not the ground truth directly, so
        # an agent's belief can end up quite different from the actual figure.
        # TASK-203 / ISSUE-003 fix: don't clip the noisy observation itself —
        # clipping every single noisy sample at 0 (when true legitimacy sits
        # near 0, which it usually does) creates a systematic UPWARD bias,
        # since only the positive half of the noise distribution survives the
        # floor (a half-normal mean of ~noise_std*0.4, not 0). Only the final
        # blended belief gets clipped to [0,1] inside update_institution_trust.
        legitimacy_noise = rng.gauss(0, cfg.institution_trust_noise)
        observed_legitimacy = self.institutions.legitimacy + legitimacy_noise
        agent.beliefs.update_institution_trust(observed_legitimacy, cfg.confirmation_bias)

        # TASK-601: re-read own recent behavior from memory each tick — this
        # is what "metacognition" means here: an introspective, possibly
        # self-servingly biased self-assessment (see cognition/metacognition.py).
        agent.metacognition.introspect(agent, self.ship.tick)

    def _apply_action(self, agent, action):
        cfg = self.config
        if action == "forage":
            base = (cfg.forage_base_amount + 3 * agent.personality.conscientiousness
                    + cfg.forage_skill_bonus_max * agent.forage_skill)
            got_food = self.ship.resources.take("food", base)
            got_water = self.ship.resources.take("water", base)
            agent.needs.food = min(1.0, agent.needs.food + got_food / 10)
            agent.needs.water = min(1.0, agent.needs.water + got_water / 10)
            agent.energy = max(0.0, agent.energy - 0.15)
            income = 0.5 * (got_food + got_water) / 10
            # economic specialization: learning-by-doing — the more an agent
            # forages, the better they get at it (diminishing marginal skill
            # gain isn't modeled, kept as a simple linear cap at 1.0)
            agent.forage_skill = min(1.0, agent.forage_skill + cfg.forage_skill_gain)

            # TASK-202: if a leader institution exists, a legitimacy-scaled tax
            # is skimmed off non-leader income into a public reserve, later
            # redistributed equally (see Simulation.step). No leader -> no tax.
            leader_id = self.institutions.leader_id
            if leader_id is not None and agent.id != leader_id:
                tax = cfg.tax_rate_base * self.institutions.legitimacy * income
                income -= tax
                self.ship.public_reserve += tax
            agent.wealth += income

        elif action == "rest":
            agent.energy = min(1.0, agent.energy + 0.25)
            agent.stress = max(0.0, agent.stress - cfg.stress_recovery * 2)

        elif action == "socialize":
            other_id = self.social.interaction_partner(agent.id, self.agent_ids, cfg.long_range_interaction_prob,
                                                        rng=self._action_rng(agent))
            if other_id is not None:
                other = self.agents[other_id]
                if other.alive:
                    target = 0.3 + 0.4 * agent.personality.empathy

                    # ISSUE-005 fix: reconciliation. Plain decay is a SYMMETRIC
                    # repair mechanism (it pulls negative trust back toward 0
                    # exactly as it fades positive trust), but in practice
                    # negative events (steal, target -0.8) hit harder and about
                    # as often as positive ones, so trust drifted only downward
                    # in practice. A deliberate positive approach to someone you
                    # currently distrust now gets an EXTRA push — repairing a
                    # damaged relationship you keep engaging with is easier than
                    # decay alone would make it, matching the real asymmetry the
                    # other direction: reconciliation takes active effort, but
                    # effort works.
                    if self.social.get(agent.id, other_id) < 0:
                        target += cfg.reconciliation_bonus
                    if self.social.get(other_id, agent.id) < 0:
                        target_other_side = target * 0.8 + cfg.reconciliation_bonus
                    else:
                        target_other_side = target * 0.8

                    self.social.nudge(agent.id, other_id, target, cfg.trust_learning_rate)
                    self.social.nudge(other_id, agent.id, target_other_side, cfg.trust_learning_rate)
                    agent.needs.social = min(1.0, agent.needs.social + 0.25)
                    other.needs.social = min(1.0, other.needs.social + 0.15)
                    agent.memory.record(self.ship.tick, "socialized", other_id, 0.3)
                    agent.mental_model.update_from_interaction(other_id, "socialized", agent.personality.empathy)
                    other.mental_model.update_from_interaction(agent.id, "socialized", other.personality.empathy)
                    agent.mental_model.update_reflected_self(0.05)
                    other.mental_model.update_reflected_self(0.05)
                    agent.mental_model.update_second_order(other_id, 0.05)
                    other.mental_model.update_second_order(agent.id, 0.05)

        elif action == "share":
            other_id = self.social.interaction_partner(agent.id, self.agent_ids, cfg.long_range_interaction_prob,
                                                        rng=self._action_rng(agent))
            if other_id is not None and agent.wealth > 2:
                other = self.agents[other_id]
                amount = min(2.0, agent.wealth * 0.2)
                agent.wealth -= amount
                other.wealth += amount
                agent.identity.observe("benefactor")
                agent.memory.record(self.ship.tick, "gave_help", other_id, 0.3)

                # TASK-401: children can't "spend wealth" (no market yet) — being
                # shared with means being fed/cared for, so it also restores
                # needs directly.
                if other.age_years < cfg.adulthood_age:
                    other.needs.food = min(1.0, other.needs.food + 0.2)
                    other.needs.water = min(1.0, other.needs.water + 0.2)

                # TASK-303: the SAME objective event ("someone gave me wealth")
                # can carry a different meaning depending on the receiver's
                # identity — a lightweight stand-in for "the same word/act
                # means something different in different groups" (doc 3,
                # point 5) without literal word/jargon tracking. An agent who
                # has come to see themselves as an "opportunist" reads
                # unsolicited help as condescension, not kindness.
                if other.identity.label == "opportunist":
                    self.social.nudge(other_id, agent.id, -0.3, cfg.trust_learning_rate)
                    other.mental_model.update_reflected_self(-0.1)
                    other.mental_model.update_second_order(agent.id, -0.15)
                    other.memory.record(self.ship.tick, "condescended_to", agent.id, 0.4)
                else:
                    self.social.nudge(other_id, agent.id, 0.6, cfg.trust_learning_rate)
                    other.memory.record(self.ship.tick, "helped", agent.id, 0.5)
                    other.mental_model.update_from_interaction(agent.id, "helped", other.personality.empathy)
                    other.mental_model.update_reflected_self(0.2)
                    other.mental_model.update_second_order(agent.id, 0.2)

        elif action == "steal":
            other_id = self.social.interaction_partner(agent.id, self.agent_ids, cfg.long_range_interaction_prob,
                                                        rng=self._action_rng(agent))
            if other_id is not None:
                other = self.agents[other_id]
                if other.wealth > 1:
                    amount = min(2.0, other.wealth * 0.25)
                    other.wealth -= amount
                    agent.wealth += amount
                    agent.identity.observe("opportunist")
                    agent.memory.record(self.ship.tick, "stole", other_id, 0.4)
                    other.identity.observe("survivor")
                    self.social.nudge(other_id, agent.id, -0.8, cfg.trust_learning_rate)
                    other.memory.record(self.ship.tick, "betrayed", agent.id, 0.9)
                    other.stress = min(1.0, other.stress + 0.2)
                    other.mental_model.update_from_interaction(agent.id, "betrayed", other.personality.empathy)
                    other.mental_model.update_reflected_self(-0.3)
                    other.mental_model.update_second_order(agent.id, -0.3)

                    # TASK-205: courts/police — only has teeth if a leader
                    # institution exists at all (Leadership.legitimacy is 0.0
                    # with no leader, so catch_probability is 0.0 too).
                    if self.law_enforcement.maybe_catch(self.institutions.legitimacy,
                                                        self._action_rng(agent)):
                        fine = agent.wealth * cfg.punishment_wealth_fraction
                        agent.wealth = max(0.0, agent.wealth - fine)
                        agent.stress = min(1.0, agent.stress + 0.15)
                        agent.memory.record(self.ship.tick, "caught_stealing", other_id, 0.6)
                        self.cumulative_thieves_caught += 1

        elif action == "spread_belief":
            other_id = self.social.interaction_partner(agent.id, self.agent_ids, cfg.long_range_interaction_prob,
                                                        rng=self._action_rng(agent))
            if other_id is not None:
                other = self.agents[other_id]
                transmit_belief(agent, other, cfg.misinformation_rate, cfg.confirmation_bias,
                                 self._action_rng(agent), tick=self.ship.tick)

        agent.last_action = action

    def _update_internal_state(self, agent):
        cfg = self.config

        # ISSUE-014: in the need-based architecture wealth is a private stock
        # of provisions, so a hungry or thirsty agent eats from it. This is
        # what gives sharing a cost and theft a payoff in need terms.
        if (self.need_based and agent.wealth > 0
                and min(agent.needs.food, agent.needs.water) < cfg.provision_eat_threshold):
            eaten = min(agent.wealth, cfg.provision_max_per_tick)
            agent.wealth -= eaten
            agent.needs.food = min(1.0, agent.needs.food + eaten * cfg.provision_need_per_wealth)
            agent.needs.water = min(1.0, agent.needs.water + eaten * cfg.provision_need_per_wealth)

        agent.needs.food = max(0.0, agent.needs.food - cfg.need_decay)
        agent.needs.water = max(0.0, agent.needs.water - cfg.need_decay)
        agent.needs.social = max(0.0, agent.needs.social - cfg.need_decay * 0.6)
        agent.needs.safety = min(1.0, max(0.0, 1 - agent.beliefs.scarcity_belief))

        scarcity_pressure = max(0.0, 0.4 - min(agent.needs.food, agent.needs.water)) * 2
        social_pressure = max(0.0, 0.3 - agent.needs.social)
        agent.stress = min(1.0, max(0.0,
            agent.stress + cfg.stress_from_scarcity_gain * scarcity_pressure
            + 0.5 * social_pressure - cfg.stress_recovery))

        agent.mood = min(1.0, max(0.0,
            0.5 + 0.5 * (agent.needs.food + agent.needs.water) / 2
            + 0.3 * agent.needs.social - 0.4 * agent.stress))

        if agent.needs.food < 0.15 or agent.needs.water < 0.15:
            agent.health -= 0.02
        else:
            # TASK-207: recovery rate gets an institutional boost scaled by
            # the leader institution's TRUE legitimacy; baseline always applies.
            recovery = health_recovery_rate(self.institutions.legitimacy,
                                             cfg.baseline_health_recovery_rate,
                                             cfg.institutional_health_bonus)
            agent.health = min(1.0, agent.health + recovery)
        if agent.health <= 0:
            agent.alive = False
            agent.death_cause = "starvation"
            self.lifecycle.cumulative_deaths_starvation += 1

        # slow personality drift under chronic stress (doc 3, point 1)
        if agent.stress > 0.8:
            agent.personality.conformity = min(1.0, agent.personality.conformity + 0.001)
            agent.personality.empathy = max(0.0, agent.personality.empathy - 0.0005)

        agent.identity.resolve()  # TASK-302: re-evaluate identity from accumulated evidence

    def step(self):
        self.ship.step()
        self.social.decay(self.config.relationship_decay)
        self.institutions.maybe_update(self.ship.tick, self.agents, self.social)

        # a sitting leader accumulates "leader" identity evidence each tick they
        # hold the role — this is what lets TASK-302's identity mechanism form
        # a leader identity without a separate bespoke code path.
        if self.institutions.leader_id is not None:
            leader = self.agents[self.institutions.leader_id]
            if leader.alive:
                leader.identity.observe("leader")

                # TASK-208 (partial): state media — the leader's belief reaches
                # far more of the population than organic rumor spread alone.
                if self.ship.tick % self.config.media_broadcast_interval == 0:
                    media_broadcast(leader, self.agents, self.institutions.legitimacy,
                                     self.config.misinformation_rate, self.config.confirmation_bias,
                                     self.rng, self.ship.tick, self.config.media_reach_fraction)

        # TASK-301: the norm agents act under THIS tick reflects LAST tick's
        # observed behavior — a norm always lags the behavior that built it.
        if self.metrics.rows:
            last = self.metrics.rows[-1]
            self.norms.update(last.get("cooperation_rate", 0.5), last.get("avg_institution_trust", 0.5))

        action_order = [agent for agent in self.agents if agent.alive]
        if self.config.agent_update_order == "shuffled":
            self.schedule_rng.shuffle(action_order)
        elif self.config.agent_update_order != "fixed":
            raise ValueError("agent_update_order must be 'fixed' or 'shuffled'")

        for agent in action_order:
            if not agent.alive:
                continue
            self._perceive_and_update_beliefs(agent)
            action = choose_action(agent, self._action_rng(agent), norms=self.norms,
                                    identity_strength=self.config.identity_feedback_strength,
                                    adulthood_age=self.config.adulthood_age,
                                    self_correction_strength=self.config.self_correction_strength,
                                    deterrence_strength=self.config.deterrence_strength,
                                    steal_scarcity_weight=self.config.steal_scarcity_weight,
                                    share_scarcity_weight=self.config.share_scarcity_weight,
                                    action_scarcity_reference=self.config.action_scarcity_reference,
                                    need_based=self.need_based,
                                    steal_relative_gain=self.steal_relative_gain)
            self._apply_action(agent, action)
            self._update_internal_state(agent)

        # TASK-401: aging + old-age mortality, evaluated after this tick's
        # actions so an agent who dies of old age still got to act today.
        for agent in self.agents:
            if agent.alive and self.lifecycle.age_and_check_senescence(
                    agent, self._action_rng(agent) if self.config.agent_rng_mode == "per_agent" else self.rng):
                agent.alive = False
                agent.death_cause = "old_age"

        # TASK-206: schooling — children get a personality development boost;
        # baseline always applies, institutional part scales with the TRUE
        # legitimacy of whatever leadership institution currently exists.
        for agent in self.agents:
            if agent.alive and agent.age_years < self.config.adulthood_age:
                apply_schooling(agent, self.institutions.legitimacy,
                                 self.config.informal_learning_rate,
                                 self.config.institutional_learning_rate)

        # TASK-401/402: birth — each eligible mother gets one independent
        # chance this tick; candidate fathers are her own local social ties
        # (see SocialNetwork.neighbors), not the whole population.
        newborns = []
        current_population = sum(1 for a in self.agents if a.alive)
        for agent in self.agents:
            if not agent.alive:
                continue
            candidate_fathers = [self.agents[b] for b in self.social.neighbors.get(agent.id, ())
                                  if b < len(self.agents)]
            lifecycle_rng = self._action_rng(agent) if self.config.agent_rng_mode == "per_agent" else self.rng
            child = self.lifecycle.maybe_reproduce(agent, candidate_fathers, lifecycle_rng, current_population)
            if child is not None:
                mother, father = agent, self.agents[child.parent_ids[1]]
                self._register_newborn(child, mother, father)
                self._configure_agent_rngs([child])
                newborns.append(child)
                current_population += 1
        self.agents.extend(newborns)
        # refresh the interaction pool: excludes anyone who died this tick,
        # includes anyone born this tick (from next tick onward)
        self.agent_ids = [a.id for a in self.agents if a.alive]

        # TASK-202: periodically redistribute the taxed public reserve equally
        # among the living population (only meaningful once a leader exists —
        # otherwise nothing was ever taxed into it).
        if self.ship.tick % self.config.redistribution_interval == 0 and self.ship.public_reserve > 0:
            alive = [a for a in self.agents if a.alive]
            if alive:
                share = self.ship.public_reserve / len(alive)
                for a in alive:
                    a.wealth += share
            self.ship.public_reserve = 0.0

        self.metrics.record(self.ship.tick, self.agents, self.social, self.ship, self.institutions,
                             self.norms, self.lifecycle, self.cumulative_thieves_caught)

    def run(self):
        for _ in range(self.config.n_ticks):
            self.step()
        return self.metrics
