# ODD+D Model Description — Ship of Fools

**Status:** initial code-grounded draft. This describes the current implementation,
not a validated theory of human behavior. Items marked **open** require a
research decision or further empirical grounding.

ODD (Overview, Design concepts, Details) is the documentation structure for
individual/agent-based models. ODD+D adds a structured account of human decision
making. This draft is intended to expose assumptions and support replication;
it is not evidence that the model reproduces a real population.

## 1. Overview

### 1.1 Purpose

The model explores how individual needs, stress, noisy beliefs, social
relationships, resource constraints, norms, identity and institutions interact
in a closed, fictional ship society. The first planned research focus is the
relationship between resource scarcity and cooperation/conflict. The current
model has not been empirically calibrated to a real population, so results are
theoretical and exploratory.

### 1.2 State variables and scales

| Entity | Important state | Scale / current representation |
|---|---|---|
| Agent | personality, needs, stress, energy, mood, health, wealth, beliefs, memories, identity, mental model, metacognition, age, alive/death cause | Individual; most traits/states are continuous values, with actions and identity labels categorical |
| Social relation | directed trust and local-neighbor membership | Directed trust values between agents; stable small-world neighbor sets |
| Institution | leader, legitimacy, public reserve | One population-level leadership institution; associated rules enable taxation, redistribution and institution-linked effects |
| Culture | `helping_norm`, `authority_norm` | Two population-level values updated from previous-tick observations |
| Ship/environment | food, water, capacity, disaster status | One closed shared environment; totals scale to founder population |
| Time | tick, age in ticks/years | Discrete ticks; `ticks_per_year` maps ticks to model years |

Exact variable definitions and default values live in
`ship_of_fools/agents/`, `ship_of_fools/configuration/config.py`, and the
respective subsystem modules. A “tick” is a model step, not a calibrated real
day or year.

### 1.3 Process overview and scheduling

One call to `Simulation.step()` follows this order (`simulation/engine.py`):

1. Advance the ship tick, regenerate resources, and possibly apply a storm shock.
2. Decay trust, reconsider leadership, and let an active leader broadcast on
   configured ticks.
3. Update cultural norms from the prior metrics row.
4. Iterate living agents in the current `self.agents` list order. For each:
   perceive noisy scarcity and legitimacy; update beliefs and metacognition;
   select one action; apply its effects immediately; update internal state.
5. Age living agents and check senescence mortality.
6. Apply schooling to living children; attempt births for eligible mothers.
7. Refresh the living interaction pool, redistribute a due public reserve, and
   record metrics.

**Scheduling:** agents act sequentially and effects are immediate, so later
agents can face a different state than earlier agents in the same tick. The
default is list/ID order; an alternative mode shuffles living agents once per
tick using an independent scheduling RNG. A paired-seed robustness comparison
is reported in `SCHEDULE_ROBUSTNESS_RESULTS.md`. The decision RNG stream remains
shared across agents, so changing order changes which agent receives each draw;
seed pairing is not full common-random-number coupling.

## 2. Design concepts

- **Emergence:** population outcomes arise from repeated agent actions and
  feedback among resources, beliefs, stress, relationships, norms and identity.
- **Adaptation:** agents change beliefs, needs, internal states, personality
  slowly under high stress, forage skill, identity and mental models. These are
  simplified update rules, not validated psychological processes.
- **Objectives:** actions are selected from state-dependent scores. Agents do
  not optimize a single explicit societal objective.
- **Learning / prediction:** beliefs blend noisy observations with prior belief;
  metacognition summarizes recent recorded behavior; forage skill rises with
  repeated foraging. Full Bayesian learning, reinforcement learning and active
  inference are not implemented.
- **Sensing:** agents receive noisy observations of scarcity and legitimacy,
  with stress-related upward scarcity bias. They do not directly use true
  scarcity in their decision score. Some institutional operations use true
  legitimacy (e.g. healthcare, schooling, law enforcement), while the agent's
  deterrence uses its own institution-trust belief.
- **Interaction:** agents interact through directed trust relationships and a
  small-world local network, with configured long-range contacts. Actions may
  affect another agent immediately.
- **Stochasticity:** default `agent_rng_mode="shared"` uses one seeded
  `Simulation.rng` for model randomness. Experimental `per_agent` mode derives
  action/lifecycle RNG streams from the master seed and stable agent ID; shared
  environmental, network-initialization, and media randomness still uses
  `Simulation.rng`. Metrics use a separate fixed-seed RNG.
- **Collectives:** population-level norms and leadership are aggregates over
  agent behavior/relationships; there are no explicit political factions or
  group memberships.
- **Observation:** metrics are population summaries, not direct measurements of
  real-world constructs. In particular, `cooperation_rate` is the share of
  living agents whose last action was `share` or `socialize`; `conflict_rate` is
  the share whose last action was `steal`. `action_*_rate` reports each of the
  six actions separately.

## 3. Details

### 3.1 Initialization

`Config` defaults to 80 founders and 500 ticks. `Simulation` initializes its
seeded RNG, ship, agents, small-world neighbor structure, social network,
institutions, norms, lifecycle and metrics. Founders receive random personality,
initial beliefs, stress and mood; their ages are sampled over the configured
founder age interval. Wealth and health start at fixed defaults. Resource
stocks/capacity are per-founder values multiplied by founder count. Network
construction and agent initialization consume the same simulation RNG stream.

### 3.2 Input data

The simulation currently has **no empirical input dataset**. Parameters are
read from `Config`; most are design assumptions rather than estimates from
human/population data. Random environmental shocks are generated internally.
Experiments should record all parameter overrides and seeds.

### 3.3 Submodels

#### Perception and belief

At each living agent's turn, true ship scarcity is perturbed with Gaussian noise
and a stress-dependent term. The resulting observation is blended with prior
scarcity belief using `confirmation_bias`. Legitimacy is separately perturbed
with Gaussian noise and blended into institution-trust belief. Final beliefs
are bounded by their belief update methods. Beliefs affect action scores; they
are not observations of ground truth.

#### Action selection

`cognition/decision.py` defines six action scores: forage, rest, socialize,
share, steal, and spread belief. Scores are adjusted by needs, personality,
beliefs, norms, identity, self-correction and institutional deterrence. Scores
are lower-bounded, exponentiated after division by a personality-dependent
temperature, and sampled as a softmax choice. Coefficients are not empirically
calibrated. Exact formulas are in `score_actions`. The share and steal scores
read the agent's scarcity belief directly (weights `share_scarcity_weight`,
`steal_scarcity_weight` in `Config`); `action_scarcity_reference` replaces the
belief with a constant in those two scores for ablation runs (ISSUE-013).

An opt-in alternative, `decision_architecture="need_based"` (ISSUE-014), drops
those two direct terms. Instead, with urgency `u = 1.2(1-food) + 1.2(1-water)`,
the forage score loses `u * scarcity_belief`, the steal score gains `u * g` and
the share score loses `u * g`, where `g` is the need value of one theft relative
to one base forage (0.4 at defaults). In this architecture wealth is a stock of
provisions: an agent whose food or water need is below `provision_eat_threshold`
eats up to `provision_max_per_tick` wealth per tick, each unit restoring
`provision_need_per_wealth` of both needs. The default remains `"heuristic"`.

#### Resource and action effects

Food and water are finite stocks with per-tick fractional-capacity regeneration
and a capacity cap. Foraging removes both types of stock, improves needs, and
raises forage skill. Rest restores energy and reduces stress. Socializing nudges
directed trust; sharing transfers wealth; stealing transfers wealth and damages
trust, may cause stress, and can trigger institution-dependent punishment.
Spreading belief transmits the sender's belief with configured distortion risk.

#### Stress, health, aging and births

Needs decay each tick. Food/water need deficits raise scarcity pressure and
stress; low needs reduce health, while otherwise health recovers at a baseline
plus a legitimacy-linked bonus. Age advances by ticks; older agents face an
increasing stochastic mortality risk. Birth depends on maternal age, needs,
stress, a per-tick probability, a living local eligible father, and a population
cap. Offspring inherit a noisy blend of parental personality and the parents'
current scarcity/institution beliefs; identity is not inherited. These rules
are not fitted to demographic data.

#### Social network, institutions and culture

The local graph is built at initialization. Trust is directed and updated by
interactions, then decays each tick. Leadership is reconsidered periodically
from the trust network. A leader enables legitimacy-scaled tax collection and
institutional effects; a public reserve is redistributed periodically. Norms
adapt toward prior-tick cooperation and institution-trust metrics. Identity
labels form from repeated behavior and feed back into action scores. These are
stylized mechanisms; courts, education, healthcare and media are intentionally
simple first slices, not detailed institutional models.

#### Metrics

Metrics are recorded each tick. Structural network/polarization metrics are
recomputed at an interval and carried forward between recomputations; a flat
segment between updates is a sampling artifact. Wealth-rank mobility is a
checkpoint-to-checkpoint rank correlation, not intergenerational mobility.
`human_capital_total` is total forage skill and is not innovation or GDP.

## 4. ODD+D decision-making summary

| Decision element | Current implementation |
|---|---|
| Decision makers | Each living agent, once per tick in list order |
| Options | Six fixed actions in `cognition/decision.py` |
| Decision process | Heuristic state-dependent scores followed by softmax sampling |
| Information | Own needs/personality/internal state and noisy/believed environmental/institutional state; social relationships and norms influence scores |
| Learning/adaptation | Belief updates, memory-based metacognition, identity feedback, personality drift under high stress, and forage-skill learning |
| Prediction | No explicit generative predictive model or future-state rollout |
| Rationale/evidence | Most coefficients and mechanisms are heuristic design assumptions; see `REFERENCES.md` |

## 5. Evaluation plan and open risks

1. Verify same-seed repeatability and invariants in code.
2. Pilot resource capacity/regeneration using calibration-only seeds to find a
   sustained intermediate-scarcity regime; do not select the regime based on
   cooperation/conflict outcomes.
3. Use disjoint final-analysis seeds and record the full configuration, seed,
   runtime/model version and per-tick outputs.
4. Assess uncertainty across seeds and robustness to plausible alternative
   schedules/model structures.
5. Do not infer that scarcity causes real-world behavior without an explicit
   empirical target and appropriate data.

**Paired-seed caveat:** conditions with the same initial seed do not necessarily
share aligned random shocks after their trajectories diverge, because branches
and interactions can consume different numbers of draws from the shared RNG.
The current same-seed counterfactual helper must not be interpreted as a strict
common-random-numbers design. Decide whether independent seed distributions are
sufficient or whether process/tick/agent-specific RNG streams are needed.

## References

- Grimm et al. (2020), ODD update: <https://doi.org/10.18564/jasss.4259>
- Müller et al. (2013), ODD+D: <https://doi.org/10.1016/j.envsoft.2013.06.003>
- Mechanism evidence levels and references: `REFERENCES.md`.
