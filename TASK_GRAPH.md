# TASK GRAPH — V0 → V6 (following the ordering in doc 3)

The AI orchestration flow for each task: **Research → Architecture → Implementation
→ Test → Review** (see `PROJECT_CONSTITUTION.md`). Dependencies are ordered
below; the previous stage must be completed before moving on to a V stage.

## ✅ V0 — Artificial Individual + minimal society (COMPLETED)
- [x] TASK-001 Agent architecture (personality, needs, stress, memory)
- [x] TASK-002 Beliefs (perception that can deviate from reality)
- [x] TASK-003 Cognition (utility-based decision making)
- [x] TASK-004 SocialNetwork (trust graph)
- [x] TASK-005 Information/rumors (belief propagation + distortion)
- [x] TASK-006 Economy (shared resource pool)
- [x] TASK-007 Environment (Ship + random shocks)
- [x] TASK-008 Simulation engine (tick loop)
- [x] TASK-009 Metrics + Gini
- [x] TASK-010 Experiment runner (multi-seed comparison)
- [x] TASK-011 Visualization (time-series plots)
- [x] TASK-012 Sanity tests

## V1 — Social Individual (deepening)
- [x] TASK-101 Neighbourhood/community structure: small-world graph (`build_neighbor_structure`),
      85% of interactions go through fixed local ties, 15% through long-range random contact
      (gossip/news propagation channel). `relationship_decay` was also lowered from 0.01 to 0.004.
      *requires: TASK-004* — **done**
- [x] TASK-102 Mental models (`cognition/mental_models.py`): each agent keeps a
      `PerceivedOther` about the others (which can deviate from the true personality and is
      distorted according to the observer's empathy). Measured with the `social_perception_gap` metric.
      *requires: TASK-101* — **done**
- [x] TASK-103 Theory of mind (simplified, single level): `reflected_self` —
      "how I think people see me" — can drift independently of the real social reputation
      (`avg_trust`) (see metrics.png). Fully nested ToM (such as "A thinks that B thinks
      about C") does not exist yet — this was left to V6.
      *requires: TASK-102* — **done (simplified)**
- [x] TASK-104 Parameter calibration — **partially completed**:
      - Resource capacity/consumption is now scaled by `n_agents`
        (`*_per_agent` config fields + `Ship.__init__`), so the balance is not
        disrupted when the population changes (previously it was balanced at n=80
        but at n=60 `true_scarcity`→0 collapsed — fixed).
      - Capacity and regeneration rates are scaled; however, in the default
        configuration scarcity can approach the ceiling in long runs. ISSUE-011
        asks for the moderate-scarcity regime to be calibrated separately and for
        the analyses to be repeated there.
      - The behavioural effect of `misinformation_rate` was not found reliable in
        the current model (ISSUE-001, REVALIDATION.md). Instead of forcing the
        effect toward a desired outcome, this result has been documented.
      *requires: TASK-006*

## V2 — Society
- [x] TASK-201 Institutions module (`institutions/leadership.py`): leadership emerges
      organically from agent interactions — the agent whose trust-weighted
      "influence score" passes a threshold that scales with the population becomes
      the leader; if no one passes it (as in the default V0/V1 case)
      **no institution forms at all**. Tracked with the `has_leader`/`institution_legitimacy`
      metrics. *requires: V1* — **done (leadership; the status of additional institutions
      is in TASK-205–208)**
- [x] TASK-202 Simple economy extension: while a leader exists, a legitimacy-scaled "tax"
      is deducted from forage income, accumulated in a common reserve, and
      periodically distributed equally to the population (`redistribution_interval`).
      There is no specialisation/price mechanism yet. *requires: TASK-006* —
      **done (only tax + equal distribution)**
- [x] TASK-203 Institutional trust ↔ Beliefs.institution_trust feedback:
      each agent sees not the institution's real `legitimacy` but its own
      noisy/biased perception (`Beliefs.update_institution_trust`). Observed behaviour:
      `avg_institution_trust` does not fully converge from the initial bias (0.6) to the
      real legitimacy level (~0.02-0.03) within 500 ticks — confirmation_bias is a
      plausible explanation of why institutional trust changes slowly, but whether this
      is intentional or accidental is not clear; it should be tracked as TASK-204.

### Not yet in V2 (separate sub-tasks for the future)
- [x] TASK-204 Examine/calibrate the convergence speed of `avg_institution_trust` — **closed, see KNOWN_ISSUES.md ISSUE-003**
- [x] TASK-205 Courts/police (`institutions/law_enforcement.py`): equipped only if a
      leader EXISTS — the probability of being caught scales with the institution's REAL
      legitimacy; deterrence, on the other hand, scales with the agent's OWN
      `institution_trust` BELIEF (a `deterrence_strength` term in the `steal` score in
      `cognition/decision.py`) — i.e. the reality/belief distinction is present here too.
      A leader forms in 3 of 5 seeds and when one forms, thieves are actually caught
      (4-12 times/run), but because legitimacy always stays low (~0.01-0.03)
      deterrence is weak — this is consistent with the project's general "fragile
      institutions" pattern, not a separate bug.
- [x] TASK-206 Education (`institutions/education.py`): children receive each tick a small
      baseline ("being raised by the village") + an extra development rate scaled by the
      institution's REAL legitimacy (conscientiousness/openness).
      If there is no leader, only the baseline rate operates.
- [x] Economy: simple specialisation (learning-by-doing) — `Agent.forage_skill`,
      increases with each forage action and raises foraging efficiency. A full
      price/labour market still does not exist, but the principle "whoever does the
      same work more becomes better" now exists.
- [x] TASK-207 Healthcare (`institutions/healthcare.py`): the health recovery rate
      consists of a baseline + a legitimacy-scaled extra bonus (same pattern as
      education/leadership). *requires: TASK-201* — **done**
- [x] TASK-208 Media (`institutions/media.py`) — **only media, religion/science
      still do not exist**: while a leader exists, a legitimacy-scaled "broadcast" every
      `media_broadcast_interval` ticks — the leader's belief reaches a much wider
      audience than organic gossip (neighbourhood + 15% long-range), with the same
      `transmit_belief` distortion mechanics.
- [x] Multidimensional culture (partial): a second axis in `culture/norms.py` —
      `authority_norm` (0=autonomy, 1=hierarchy/obedience) — formed from the previous
      tick's `avg_institution_trust`, fed back into the `steal`/`spread_belief` scores
      of agents with high conformity.
      Of the 7 axes proposed by doc 1, only 2 (helping_norm, authority_norm) exist;
      individualism/collectivism, tradition/change, economic preferences etc. still do not.
- [ ] Religion/science institutions are still not modelled (the remainder of TASK-208).
- [ ] A real price/labour market still does not exist — there is only simple forage specialisation.

## V3 — Culture
- [x] TASK-301 Norm formation (`culture/norms.py`): `helping_norm` — the population's
      perception of "is mutual aid normal here?" — starting from scratch (0.5, neutral)
      and forming spontaneously by tracking the previous tick's `cooperation_rate`, then
      fed back into the `share`/`steal` scores of agents with high conformity (the more
      the norm has shifted toward "selfish", the more a conformist agent becomes prone
      to stealing). *requires: V2* —
      **done (only a single norm dimension — identity/language do not exist yet)**
- [x] TASK-302 Identity ("I am an X"): `agents/identity.py` — identity starts from
      scratch (`label=None`), forms after at least 5 repeated behaviours
      (leadership/helping/theft/victimisation) have accumulated, and once formed
      reinforces that behaviour with the `identity_feedback_strength` coefficient
      (sunk-cost). **Verified by a parameter sweep**
      (`KNOWN_ISSUES.md` ISSUE-004): as the coefficient increases from 0.0 to 0.5,
      `avg_trust` and `positive_relationship_rate` fall monotonically at all 5
      levels — a real, dose-dependent effect. (This is a 5-seed sweep; at n=30 only
      the 0.0/0.5 endpoints were re-tested, the intermediate doses were not —
      `REVALIDATION.md`.)
      *requires: V3* — **done**
- [x] TASK-303 Simple "jargon" — the same objective action acquiring a different
      subjective meaning in different identities/groups: an agent with
      `identity.label == "opportunist"` reads a `share` (help) action directed at it
      not as a trust increase but as condescension (the sign of the trust nudge is
      reversed). Not a real word-based language model — a behavioural approximation
      of doc 3, point 5. *requires: TASK-302* — **done (simplified)**

### Observed open question (after V3)
The `identity_feedback_strength` effect and the consensus mechanics were later
re-tested with multiple seeds; the results and the limits of interpretation are
in `REVALIDATION.md`.

## V4 — Evolution (generations)
- [x] TASK-401 Birth/ageing/death cycle (`population/lifecycle.py`):
      founders start at diverse ages between 18 and 50 (not a single cohort);
      old-age mortality risk increases with age after `elderly_age`(60);
      birth occurs when the mother is of suitable age/has her needs met/has low stress
      AND a "father" of suitable age is found in her local social environment
      (not a random mate). `max_population_multiplier` is a carrying-capacity
      safety valve. *requires: V3* — **done**
- [x] TASK-402 Cultural transmission (partial — at the "family" level): the child's
      personality inherits the parents' blended+mutated ("nature") personality, and its
      beliefs (`scarcity_belief`, `institution_trust`) inherit the parents' CURRENT
      worldview ("nurture"). **Identity is NEVER inherited** — TASK-302's rule that
      "identity arises from lived experience" applies to children too. There is no
      society-wide cultural absorption (school/broad socialisation), only parental
      transmission. *requires: TASK-301, TASK-302* —
      **done (family level only)**

### Observed emergent finding (after V4, default config)
80 founders (of diverse ages, all of reproductive age) → in the first ~150 ticks the
population jumps to 110 ("baby boom", because all the founders are of suitable age at
the start) → because `resource_capacity` is fixed only according to the FOUNDER
population (80) (see `ARCHITECTURE.md`), resource demand exceeds supply →
`true_scarcity` locks at 1.0 around tick 250 and stays there until 500 → even when the
population falls back to ~88 (still above the founder capacity) no recovery is seen →
stress, conflict and distrust all keep rising. This is the kind of "population boom →
exceeding carrying capacity → collapse" scenario that doc 1 expected.
In a follow-up run with 2000 ticks and 10 seeds, population collapse was observed in
10/10 seeds. In the condition where capacity was doubled, the collapse was largely
prevented. The result and its limits are recorded in ISSUE-007.

## V5 — Experimental Laboratory
- [x] TASK-501 Counterfactual world (`experiments/counterfactual.py`):
      `run_seeds()` — runs the same config with N different seeds and gives the
      distribution; `run_paired_counterfactual()` — runs two worlds with the same seed
      and a single parameter difference and reports the **first divergence tick**
      (doc 3, "World A vs World B"). *requires: TASK-010* — **done**
- [x] TASK-502 Causal narrative extraction (`experiments/causal_narrative.py`):
      walks through a run's metric history, finds the tick at which predefined
      warning signs (resource depletion, stress, trust, conflict, loss of leadership,
      population decline) were FIRST triggered, and reports them in chronological order.
      **This is not evidence of causality** — only the observed ordering
      (PROJECT_CONSTITUTION rule 4). The leadership signal distinguishes never
      having a leader form from the leader later disappearing (ISSUE-008).

### The finding that closed ISSUE-007 (see `run_v5_lab.py`, `KNOWN_ISSUES.md`)
10 seeds × 2000 ticks, 3 conditions: (A) default config → **100% fall below the founder
population**, 30% nearly go extinct; (B) when `birth_rate_base` is lowered
(0.008→0.003) it **gets even worse** (100% fall to a population of ≤5 — the naive
intuition turned out wrong); (C) when `resource_capacity_per_agent` is doubled
(75→150) **the collapse almost completely disappears** (0% fall to a population of ≤20,
most stabilise at the carrying capacity (144)). The real bottleneck turned out to be
resource capacity, not the birth rate — exactly the kind of finding V5 is supposed to
produce.

## V6 — NeuroAI
- [x] TASK-601 Metacognition (`cognition/metacognition.py`): at each tick each agent
      re-reads its own behaviour over the last ~40 ticks from its own memory
      ("gave_help" vs "stole" events) — and this reading is distorted by a
      self-serving bias in agents with low openness/high stress. The result is fed back
      into the `share`/`steal` scores of agents with high `conscientiousness`
      (self-correction); agents with low conscientiousness largely ignore this signal
      (doc 2, point 2: self-evaluation does NOT ALWAYS change behaviour).
      *requires: V3* — **done**
- [~] TASK-602 Second-order theory-of-mind + predictive processing —
      **only the first half was done**: a separate `they_probably_think_of_me` field
      was added to `MentalModel` for each (agent, other-agent) pair ("how I think this
      SPECIFIC person sees me" — a relationship-specific estimate, unlike the
      population-wide `reflected_self` of V1). Fully nested ToM (3-link chains such as
      "A thinks that B thinks about C") and predictive processing/active inference
      replacing `cognition/decision.py` were **not done** — this is a separate task of
      much larger scope that would require completely replacing the current
      utility/softmax architecture; it should be split off as TASK-602b and taken up in
      the future.

## PLANNED (TASK-602b not yet started; the first slice of TASK-701 done)

### TASK-602b — Predictive processing / active inference (NeuroAI core)
**Status: planned, no code written.** This is the weakest part of the project's "Neuro"
side so far — the current `cognition/decision.py` uses pure utility/softmax scoring,
and there is no neuroscience-inspired computational mechanism.

Rough plan:
1. `cognition/predictive_processing.py` — a decision module that is an ALTERNATIVE to
   decision.py (without deleting it): the agent should have a "generative model" at
   every moment (how it expects the world to be — via the `needs`, `beliefs`, `social`
   state), and the difference between the actual observation and this expectation
   ("prediction error") should be computed.
2. Action selection should be done, instead of the hand-written utility scores used
   now, according to the principle "which action reduces the expected prediction error
   the most" (a simplified version of active inference).
3. A `cognitive_architecture: str` config field should be added to `Simulation`
   ("utility" | "predictive_processing") so that one can choose between the two — per
   TASK_GRAPH's own rule (PROJECT_CONSTITUTION rule 7: do not trust a single run) the
   two should be run COMPARATIVELY in the same scenario and the emergent results
   (stress, cooperation, collapse dynamics) compared.
4. Documentation for each mechanism per PROJECT_CONSTITUTION rule 4: which
   neuroscientific phenomenon it represents, which simplification was made.
- **Dependency**: none, can be started independently; can be added on top of the
  existing `Agent`/`Beliefs` structure without breaking it (the architecture was
  already designed to be modular so as to allow this — see `ARCHITECTURE.md`).
- **Estimated scope**: larger than a single V-stage in this project (e.g. V3) —
  requires a separate round of work in its own right.

### TASK-701 — Interactive visualisation / dashboard
**Status: FIRST SLICE DONE (see "Done" below); what remains open is in
`KNOWN_ISSUES.md` ISSUE-010.**

#### Done
- `visualization/dashboard_export.py`: a separate instrumented loop WITHOUT TOUCHING
  the core engine (it calls `Simulation.step()` directly and takes a snapshot of the
  sampled founder agents every 10 ticks) + an export of the last-tick trust network.
  Output: a single JSON bundle (~850 KB, 80 agents/500 ticks).
- `visualization/dashboard_template.html` + `run_dashboard.py`: a single-file HTML
  dashboard generator (`python3 run_dashboard.py --agents 120 --ticks 800`).
  Three tabs: **Population** (metric selector, tick-range sliders, hover
  tooltip), **Agent Inspection** (18 sampled agents; personality radar chart
  initial-vs-current; time series of the selected field), **Social Network** (D3
  force-directed graph; node colour=identity label, edge colour=trust
  sign, thickness=|trust|).
- Published as a Claude artifact (private, until the owner shares it).

#### Not done (from the original plan)
- Full per-agent export for all agents (only 18 samples).
- Animation/slider of the social network over time (only the last tick).
- Side-by-side comparison of two runs/counterfactual worlds.
- End-to-end visual verification in a real browser (see ISSUE-010).

#### Remaining dashboard work
The first slice has been implemented; the scope and verification limits are kept in
ISSUE-010. The old plan is preserved in the items below as a historical reference.

Rough plan:
1. A single-file HTML/JS-based dashboard (compatible with Claude's artifact/publish
   flow) — it should read `metrics.csv` and draw the time-series charts
   interactively (zoom, showing the value on hover over a tick).
2. Individual agent inspection panel: when an agent id is selected, it should be able
   to show that agent's personality/needs/beliefs/identity/mental_model state and its
   change over time (`Agent` already holds this data, only the export is missing).
3. Social network visualisation: it should draw `SocialNetwork.trust` as a graph
   (node=agent, edge=trust, colour=positive/negative) — identity clustering and
   leadership formation in particular would be visually much more striking.
4. An "agent snapshot" exporter will be needed to make `Simulation` export the full
   agent-level state at every tick (currently only population-average metrics are
   recorded, `metrics/tracker.py`) — this would significantly increase storage size
   (n_agents × n_ticks × number of fields), so it would probably make sense to do it
   only for the last N ticks or with sparse sampling (once every 10 ticks).
- **Dependency**: none, can be started independently.
- **Estimated scope**: medium — smaller than TASK-602b but still requires a separate
  round of work in its own right (especially the agent-snapshot exporter).

### Honest status after V6
The whole V0→V6 plan in `TASK_GRAPH.md` has been implemented at least at the
first-slice level. Institutions are now 4/7 (leadership, courts/police, education,
healthcare, media — religion/science still do not exist), culture is 2-dimensional
(out of 7), the economy has simple specialisation (not a full market). Sensitivity
analysis was performed at both the single-parameter (Morris) and the limited-interaction
(2x2 factorial) level; the scale test was completed and a real performance bug was
fixed. The two largest remaining jobs were planned above as TASK-602b and TASK-701.

## Systematic sensitivity analysis and scale test (after V6)

### Systematic sensitivity analysis: interaction test added
`experiments/sensitivity.py::factorial_interaction` — a 2x2 factorial design for the
two most influential parameters (`resource_capacity_per_agent`, `food_regen_rate`)
(`run_interaction_test.py`). **Finding**: the interaction on `true_scarcity` (-0.391)
is almost TWICE as strong as the main effect of `food_regen_rate` alone (-0.195) — that
is, when capacity is already high the effect of the regen rate becomes much stronger
(at low capacity the benefit of increasing regen is limited, there is a hard ceiling).
There is also a diminishing-returns type of interaction on `population` (-9.925). This
is exactly the kind of finding that a purely one-at-a-time (Morris) screen would MISS
and only a factorial design could catch — concrete evidence of why a full Sobol would
be valuable, but it has still been done for only 1 pair (a full sweep over the
C(18,2)=153 pairs of 19 parameters was not done — it would be too expensive).
- **Sensitivity analysis** (`experiments/sensitivity.py`, `run_sensitivity.py`):
  a Morris-type "elementary effects" screen instead of a full Sobol — 19 parameters,
  each perturbed alone and measured with 4 seeds. **`resource_capacity_per_agent`
  and `food_regen_rate` turned out to be by far the two most influential parameters** —
  this confirmed the ad-hoc finding of ISSUE-007 with a completely independent method.
  The method's known limitation: it does not capture INTERACTION between parameters
  (only single effects).
- **Scale test** (`run_scale_test.py`): measured over the range 100→10,000 agents.
  In the first round (100-1600 agents) it came out close to linear (exponent≈1.05), but
  in the 1600-10,000 range genuinely super-linear behaviour appeared (exponent≈1.26).
  The root cause was isolated: `SocialNetwork.random_acquaintance` filtering the whole
  population on every call (`[x for x in agent_ids if x != a]`) — this was
  **a real performance bug, and was fixed** (reject-and-retry, O(1) expected). After
  the fix the exponent fell from 1.26 to 1.09. At n=10,000 it is now ~0.35s per tick
  (500 ticks ≈ 3 minutes) — doc 1's "10,000 agents" target is now practically
  reachable.


## REMAINING WORK INVENTORY (historical note after V6; the current status is in the sections above)

This list was derived by scanning the code, not from memory (the grep results were
shown in the session). The order of priority is our suggestion, not definitive.

**A. AI orchestration was never set up (the project's original claim).** The folder was
not a git repo when this inventory was written (`git init` was done on 2026-10-07).
There are no separate research/architecture/coding/review roles, no branch discipline,
no independent cross-checking; all the work was done in a single continuous flow, and
the "review" was the same flow finding its own mistakes afterwards.

**B. TASK-602b — predictive processing / active inference.** No code. In addition, the
neural layer in doc 1 §2A (attention, working memory, sleep, habit formation) and the
learning methods in §8 (RL, Bayesian updating, imitation, evolutionary adaptation) are
largely absent — there are only belief blending and `forage_skill`. Among cognitive
biases only those resembling confirmation/negativity/self-serving exist; anchoring,
availability, loss aversion etc. do not.

**C. Scientific grounding is missing.** `REFERENCES.md` records the mechanism–source
mapping and the evidence level; unverified citations are marked, and most of the
mechanisms are heuristic design choices. Literature review, finding valid sources and
empirical calibration are still open work.

**D. Measurement and statistics.** Polarisation, network centralisation, a few measures
of social cohesion and wealth-rank mobility were added; `human_capital_total` is not
innovation. The statistical tools and the n=30 re-testing are documented in
`REVALIDATION.md`. Not all parameter pairs were swept; the remaining sample and regime
limitations are tracked in ISSUE-011/012.

**E. No group/faction structure.** No alliance, group formation/leaving, or faction code.
Therefore the emergent phenomena of doc 1 (political factions, rebellion, revolution,
cult-like groups, migration) cannot currently be detected, only tracked indirectly.

**F. Economy/technology.** No trade, price, labour market, unemployment (a "no market
yet" note in `engine.py`). Technology evolution (doc 3 §6) was never done. Religion and
science institutions do not exist. In culture only 2 of the 7 axes exist
(`helping_norm`, `authority_norm`). Deception/manipulation/betrayal actions do not exist
beyond `steal` and gossip distortion. No fully nested ToM.

**G. Scale.** Only the time per tick was measured (20/15 ticks, births off). Whether the
DYNAMICS of 500 ticks at 10,000 agents remain reasonable, and memory usage, were not
tested.

**H. ISSUE-010** — the dashboard was not verified in a real browser (see KNOWN_ISSUES.md).

**I. Test coverage.** There is a single sanity test module; there are no regression
tests for emergent behaviour, CI, or coverage measurement yet. Since the number of tests
may change over time, no fixed count is kept here.


### Historical inventory update
- **C — partially done.** `REFERENCES.md`: 5 citations were verified by web search, 4 are
  marked as NOT VERIFIED; every mechanism was honestly classified as [E]/[T]/[S]. Result:
  **most of the mechanisms are [S]** (heuristic), none is empirically calibrated. This
  gap was NOT CLOSED, it only became visible; the calibration work is still open.
- **D — partially done.** Added: polarisation (belief+wealth), network centralisation,
  reciprocity/clustering/giant component, wealth-rank mobility, `human_capital_total`;
  `experiments/statistics.py` (CI, Welch, Cohen d, Bonferroni); 4 old findings were
  re-tested with n=30 (`REVALIDATION.md`). **Not done:** innovation/GDP (there is no
  mechanism in the model, it was not invented), intergenerational mobility, a holistic
  definition of social cohesion, re-testing of the remaining findings (ISSUE-012), the
  moderate regime (ISSUE-011).

## Start of implementation of the academic research plan (2026-10-04)

- `ACADEMIC_RESEARCH_PLAN.md`: ODD/ODD+D, code verification, pattern-oriented
  evaluation, seed and experiment principles.
- `ODD_D.md`: a first ODD+D draft documenting the current agent decisions, schedule and
  operational metric definitions according to the source code.
- `run_regime_calibration.py`: capacity/regeneration pilot. The first 16 cells × 4 seeds
  and the follow-up 2×2 × 20 seeds were done. Because moderate scarcity did not
  replicate stably across seeds, ISSUE-011 is open; the results are in
  `ACADEMIC_RESEARCH_PLAN.md` and `output/regime_calibration_*.json`.
- `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md` and
  `run_resource_factorial.py`: a pre-defined 2×2 factorial protocol and runner
  (30 seeds/cell, independent seed blocks, seed-level bootstrap uncertainty
  intervals). The final run was completed; the report is
  `RESOURCE_STRESS_RESULTS.md`, the raw files are in `output/resource_factorial/`.
- Verification: the same-seed reproducibility test, the factorial smoke test and a small
  CLI smoke run passed. The full `test_basic.py` was not completed in this environment
  because SciPy (added to `requirements.txt`) was not present.
- The update-order robustness analysis was completed: `agent_update_order` can be chosen
  as fixed or shuffled per tick. Factorial contrast differences were computed with the
  same 120 seed-condition pairs; the bootstrap interval of nine differences covered
  zero. The directions are the same in the two schedules. The report is
  `SCHEDULE_ROBUSTNESS_RESULTS.md`, the raw files are in `output/schedule_robustness/`.
- The follow-up that reduces RNG coupling was completed: 240 simulations running the
  same seeds in fixed/shuffled order with `agent_rng_mode="per_agent"`. Nine factorial
  effect differences covered zero; the directions were preserved. `shared` remained the
  default. The report is `AGENT_RNG_ROBUSTNESS_RESULTS.md`, the raw data is in
  `output/agent_rng_robustness/`.
- The old identity-feedback finding was re-tested within the resource regimes:
  2×2×2, 30 paired seed blocks/cell, 240 runs in total. Trust decreased and conflict
  increased; the conflict increase was larger at low capacity. The report is
  `IDENTITY_RESOURCE_RESULTS.md`, the protocol is `EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md`.
  Intermediate doses and an explanation of the Gini/population mechanism are open
  follow-up work.

## Review of the formula dependence of the findings (2026-10-07)

When the documents and `cognition/decision.py` were read together, it was seen that the
primary results of the two main experiments are written directly into the decision
formula (ISSUE-013).

- [x] The scarcity-belief coefficients in the `steal`/`share` scores were moved to
      `Config`; the link can be severed with `action_scarcity_reference`. The default
      behaviour is bit-for-bit identical.
- [x] Action-share metrics (`action_*_rate`) were added.
- [x] Sanity tests: `tests/test_scarcity_link_ablation.py`.
- [x] The ablation protocol was written before the run:
      `EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md` (2×2×3, 30 seed blocks, 360 runs).
- [x] Ablation run and report: `SCARCITY_LINK_ABLATION_RESULTS.md`.
- [x] Label/action distribution of the identity experiment (post hoc): `run_identity_label_followup.py`.
- [ ] A separate ablation for identity feedback (label → score term) — no protocol.
- [ ] Re-testing the ISSUE-007 birth-rate finding with n≥30 (ISSUE-012).
- [ ] Examining the between-seed regime divergence in the `120/0.016` cell as a separate question.
- [ ] Decision on the `shared` / `per_agent` RNG default.

## Need-based decision architecture (2026-10-07)

ISSUE-014: wealth did not satisfy any need, so the link between stealing and scarcity
could be established only with a hand-written coefficient.

- [x] `decision_architecture` switch; in the `"need_based"` arm, edible provisions and
      urgency × payoff scores. The default did not change.
- [x] Sanity tests: `tests/test_need_based_decision.py`.
- [x] Protocol before the run: `EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`
      (2×2 resource × 2 architectures, 30 seed blocks, 240 runs).
- [x] Run and report: `NEED_BASED_DECISION_RESULTS.md` (2026-10-09). The resource →
      conflict relationship is in the same direction but about one eighth of that in the
      `intact` arm.
- [x] Provisions and the decision rule were split into separate switches
      (`provisions_edible`, `need_based_scoring`); `need_based` trajectories are
      bit-for-bit identical.
- [x] Decomposition protocol before the run: `EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`
      (2×2 resource × 2×2 decision, 30 seed blocks, 480 runs).
- [x] Decomposition run and report: `PROVISION_SCORING_FACTORIAL_RESULTS.md` (2026-10-09).
      The difference belongs to the scoring form; the provisions effect cannot be distinguished.
- [x] `avg_min_need`, `need_deficit_rate` metrics; ISSUE-015 opened
      (`true_scarcity` measures store fullness, agents are well fed even at the ceiling).
- [x] Deprivation pilot (`run_deprivation_pilot.py`): in fixed order no lasting
      deprivation arises; in shuffled order regeneration 0.004 was chosen. ISSUE-016
      opened (fixed order produces priority by agent ID under scarcity).
- [x] Deprivation protocol before the run: `EXPERIMENT_PROTOCOL_DEPRIVATION.md`
      (2×2 resource × 2×2 decision, shuffled order, 480 runs).
- [x] Deprivation run and report: `DEPRIVATION_RESULTS.md` (2026-10-09). Deprivation
      lowers the `steal` share in the original scoring and raises it in the need-based scoring.
- [ ] In the need-based scoring, multiplying the `forage` payoff by the stores belief
      keeps agents from foraging when deprived (a design weakness); a separate protocol
      for an alternative payoff expectation.
- [ ] Verifying the ISSUE-016 diagnosis with n≥30; decision on the default order.
- [ ] Sensitivity to the `provision_*` parameters (especially `provision_max_per_tick`).
- [ ] Mass conservation in foraging: explicit separation of the eaten and the stored share.
- [ ] A null model for Gini (random transfer only) — `REFERENCES.md` #15.
- [ ] Comparison with Epstein's (2002) decision rule ("docking") — `REFERENCES.md` #10–11.
