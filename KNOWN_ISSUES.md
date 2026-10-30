# KNOWN ISSUES / OPEN THREADS

This file is the technical-debt list that every AI in the "review agent" role
must check before moving to a new V-stage (a simplified version of the
`DECISIONS/` folder in doc 4). When an item is closed it is not deleted from
here — it is marked "closed" and how it was closed is noted, so that the
decision history is not lost.

## Open

### ISSUE-010 — The dashboard has not been verified end to end in a real browser + known scope limits
- **Where**: `ship_of_fools/visualization/dashboard_export.py`, `dashboard_template.html`, `run_dashboard.py`
- **What was verified**: (a) the syntax of the embedded JS is clean under
  `node --check`; (b) it was checked programmatically in Python that the data
  bundle (`meta`, `timeseries`, `agents`, `network`) contains ALL the fields
  the JS reads; (c) the `test_dashboard_export_bundle_shape` test passes.
- **What was NOT verified**: because of the sandbox's network restriction, the
  Chart.js/D3 CDN scripts could not be loaded, so the page was not rendered
  and visually inspected in a real browser. There may be runtime errors (e.g.
  the size of charts created in hidden tabs — a `resize()` call was added
  against this but was not seen to work).
- **Known scope limits** (not bugs, deliberate first-slice decisions):
  1. The agent inspection panel covers only **18 sampled founder agents** (not
     all agents; later-born agents are not included) — a full per-agent export
     would have made the size much larger.
  2. The social network is only the graph of the **last tick** (no time
     slider/animation), limited to the ~90 best-connected agents.
  3. Zooming is by two range sliders, not drag-and-drop.
  4. Single run — there is no side-by-side comparison of two worlds
     (counterfactual).
  5. Two CDN dependencies (Chart.js 4.4.4, D3 7.9.0) — it does not open offline.
- **Proposed closure**: open the page in a real browser and visually check the
  three tabs; note any bugs found here and fix them.
- **Related task**: TASK-701 (`TASK_GRAPH.md`)
- **Status**: **open**.

### ISSUE-011 — Most experiments run in the "collapse regime" (ceiling effect)
- **Where**: the default config; `run_sensitivity.py`, `run_revalidation.py`
- **Symptom**: in the default regime with n=60/300 ticks, `true_scarcity` =
  0.996 ± 0.007 (stuck at the ceiling); `identity_formed_rate` also sticks at
  1.0 (ISSUE-004). A metric at its ceiling cannot reveal a parameter that
  acts on it.
- **Consequence**: (a) the whole sensitivity screening was carried out in this
  regime, so the ranking may differ in another regime; (b) the findings on
  `identity_feedback_strength` and `reconciliation_bonus` were tested only in
  this regime.
- **Partial mitigation**: `misinformation_rate` was also re-tested in the
  resource-abundant regime (`REVALIDATION.md` 4b) — there is no effect there
  either, so that result does not depend on the regime.
- **Regime pilot and final factorial (2026-10-04)**: with
  `run_regime_calibration.py`, 16 cells × 4 seeds were first screened; the
  `90 / 0.019` cell ranked first. However, in the 2×2 follow-up on a new seed
  block (`n=20`/cell, last 100 ticks), this setting gave a mean scarcity of
  0.853 and was not suitable. The `120 / 0.016` setting gave a mean of 0.582,
  a between-seed SD of 0.189 and a 4.1% share of ticks spent at the ceiling;
  even so, in only 11 of 20 seeds was the last-window seed mean within the
  0.30–0.60 band. The 2×2 final experiment then fixed (30 seeds/cell, last 100
  ticks) gave scarcity of 0.978 [0.963,0.992] for `90/0.016` and 0.493
  [0.431,0.555] for `120/0.016`. In 17/30 of the `120/0.016` seeds the
  scarcity seed mean was within the 0.30–0.60 range; between-seed SD 0.178.
  This yielded a factorial study free of the ceiling regime, but did not show
  that a stable "intermediate scarcity" regime forms in every seed.
  Cooperation/conflict and contrasts: `RESOURCE_STRESS_RESULTS.md`; raw
  results `output/resource_factorial/`.
- **Earlier finding in the new regime (2026-10-05)**: `identity_feedback_strength`
  0→0.5 was crossed with the resource 2×2 (30 identical seed blocks/cell). The
  decline in trust and the rise in conflict point the same way in all four
  regimes; the conflict effect is larger at low capacity. Details in
  `IDENTITY_RESOURCE_RESULTS.md`. This result does not verify all the earlier
  parameter findings in the new regime; it belongs to the selected identity
  contrast.
- **Proposed closure**: limit the scope to this final factorial, and decide,
  according to the research question, which findings previously obtained in
  the ceiling regime need to be re-tested; do not automatically repeat the
  general parameter screening.
- **Status**: **open — the first regime comparison is complete; the robustness
  of the earlier findings in the new regimes must be assessed separately**.

### ISSUE-012 — Some findings are still small-sample / without confidence intervals
- **What**: the sensitivity screening (4 seeds × 19 parameters), the 2×2
  interaction test (4 seeds), the ISSUE-007 rates (10 seeds), ISSUE-006 (1
  seed), the intermediate doses of ISSUE-004, the scale test.
- **Re-verified** (n=30, Welch, Bonferroni): ISSUE-001, 004 (endpoints only),
  005 and the resource-capacity finding — see `REVALIDATION.md`.
- **Proposed closure**: re-run the rest as well with n≥30 and confidence
  intervals; for ISSUE-007, 2000 ticks × 30 seeds ≈ 15 min.
- **Status**: **open**.

### ISSUE-013 — Primary experiment results are written directly into the decision formula
- **Where**: `cognition/decision.py` (`score_actions`), `metrics/tracker.py`
- **What**: the `steal` score contains `+0.9 × scarcity_belief` and the `share`
  score `−0.5 × scarcity_belief`; and `conflict_rate` is the share of agents
  whose last action was `steal`. The H2 result of the resource experiment
  ("favourable resources → less `steal`, more `share`/`socialize`") is
  therefore at least partly a read-back of the formula; it cannot be presented
  as an emergent finding. The same applies in the identity experiment: the
  `opportunist` label adds `identity_feedback_strength` directly to the
  `steal` score, the direction of the net effect depends on which label
  dominates, and the label distribution was not recorded in the first run.
- **Done (2026-10-07)**:
  1. Two coefficients were moved to `Config` (`steal_scarcity_weight`,
     `share_scarcity_weight`) and `action_scarcity_reference`, which severs
     the link, was added. The defaults preserve the old behaviour bit for bit
     (the trajectory summary is identical before/after the change in three
     configurations).
  2. The separate shares of the six actions (`action_*_rate`) were added to
     the metrics.
  3. Ablation experiment: `EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`,
     results `SCARCITY_LINK_ABLATION_RESULTS.md`.
  4. Post hoc follow-up for the label/action distribution of the identity
     experiment: `run_identity_label_followup.py`, results in an additional
     section of `IDENTITY_RESOURCE_RESULTS.md`.
- **Ablation result (2026-10-07, 360 runs)**: when the direct term is cut, the
  capacity effect changes sign on the conflict measure (`intact` −0.101;
  `zero` +0.012; `fixed` +0.014; the intervals exclude zero). On the
  cooperation measure, 14–25% of the effect remains. The effects of the
  resource regime on trust, stress, the help norm and the label composition
  also vanish or fall to one tenth in the ablation. H2 is not an emergent
  finding but a verification of the decision rule.
- **Identity follow-up (post hoc)**: in the cell where the `steal` increase is
  largest, the `opportunist` share does not increase; the increase is
  consistent with the fixed bonus. The Gini increase (+0.10–0.11) is the same
  in the four regimes and cannot be explained by the stealing rate.
- **Findings not hand-written, candidates for emphasis**: the dispersion of
  seeds over the 0.085–0.819 scarcity range in the `120/0.016` cell; the fact
  that lowering the birth rate worsens the collapse (ISSUE-007, still 10
  seeds — ISSUE-012); the fact that resource abundance does not lower Gini
  and identity feedback raises Gini; the RNG matching/update-order methods
  study.
- **Proposed closure**: fix, in light of the ablation result, how H2 is
  reported (with the "direct term" and "indirect channel" shares separate);
  evaluate a similar ablation for the identity effect under a separate
  protocol.
- **Status**: **open**.

### ISSUE-014 — Wealth satisfies no need; `steal` cannot relieve scarcity
- **Where**: `simulation/engine.py` (`_apply_action`), `cognition/decision.py`
- **What**: `wealth` is read/written only in: `forage` income, `share` and
  `steal` transfers, taxation/redistribution, penalties, birth cost and the
  `wealth > 15` threshold in the `share` score. Wealth **cannot be converted**
  into food or water (there is no market). The food/water need is met only by
  `forage` (and, for children, by a `share` made to themselves).
- **Consequence**: (a) An agent cannot relieve its hunger by stealing; there
  is no path in the model by which scarcity would make stealing "rational".
  The direct `scarcity_belief` term in the `steal` score (ISSUE-013) was
  hand-written in place of this missing link. (b) Gini measures the
  distribution of a number that has no effect on survival; pairwise transfer
  of a conserved quantity alone produces high inequality (`REFERENCES.md`
  #15), so Gini findings should be read against a null model.
- **Proposed closure**: an alternative decision architecture (that does not
  change the default): actions "advertise" need satisfaction (The Sims
  pattern, `REFERENCES.md` #19–20), `steal` transfers food/water, or wealth
  can be converted into the need. Then the scarcity → stealing relation
  arises from need, not from a coefficient, and its direction is not
  pre-written. This needs a separate protocol and a `Config` switch.
- **Done (2026-10-07)**: `decision_architecture="need_based"` was added
  (default `"heuristic"`; the old trajectories are bit-for-bit identical).
  Wealth can be eaten for a need below the threshold; the
  `forage`/`steal`/`share` scores are computed as urgency × yield. Tests in
  `tests/test_need_based_decision.py`. Protocol
  `EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`, results
  `NEED_BASED_DECISION_RESULTS.md`. The `avg_wealth` metric was added.
- **Result (2026-10-09, 240 runs)**: in the `need_based` arm, the capacity
  effect is −0.012 [−0.013, −0.010] on the conflict measure (`intact` −0.098)
  and +0.016 on cooperation (`intact` +0.092): same direction, about one
  eighth to one sixth of the magnitude. The response of wealth and Gini to the
  resource regime has opposite signs in the two architectures: in the `intact`
  arm the scarcest cell is the richest cell (wealth accumulates because it
  cannot be eaten). Read together with the ablation, the magnitude of the
  resource → conflict effect changes by about a factor of eight depending on
  the decision rule.
- **Decomposition (2026-10-09)**: the two parts were split into the
  `provisions_edible` and `need_based_scoring` switches; 2×2×4 protocol
  `EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`.
- **Decomposition result (480 runs)**: the difference belongs to the score form
  (on the conflict capacity contrast the main effect of score is +0.082
  [+0.076, +0.089]); the main effect of provisions is indistinguishable
  (+0.003 [−0.002, +0.007]). The earlier interpretation that tied the
  wealth/Gini sign change to provisions was corrected. Provisions are
  ineffective because agents rarely go hungry (ISSUE-015). Report:
  `PROVISION_SCORING_FACTORIAL_RESULTS.md`.
- **Remaining**: sensitivity to `provision_eat_threshold` (of limited meaning
  until ISSUE-015 is resolved); mass conservation in foraging. No decision
  was made on the default architecture.
- **Status**: **open**.

### ISSUE-015 — `true_scarcity` measures how full the stores are, not deprivation
- **Where**: `economy/resources.py` (`true_scarcity`), `simulation/engine.py` (`forage`)
- **What**: `true_scarcity = 1 − stock/capacity`. In the diagnostic run (5
  seeds, exploratory), in the 90/0.016 cell where scarcity is at the ceiling
  (≈1.0), the agents' mean lowest need is 0.80, and the share of agents with
  a need below 0.4 is 4%. That is, the agents are well fed while the measure
  is at its maximum.
- **Why**: the regeneration flow is several times the need (capacity 7200 ×
  0.016 ≈ 115 units/tick; ~30 units/tick suffice to feed ~100 agents). The
  stores are nevertheless depleted because one foraging takes 5–12 units and
  the need is clipped at 1.0; the excess is lost. Consistent with the zero
  starvation deaths in ISSUE-006.
- **Consequence**: all the resource experiments measure the response to the
  agents' **belief** about the store indicator, not the response to real
  deprivation. The "ceiling regime" in ISSUE-011 is likewise an empty-stores
  regime, not a hunger regime. That stress and population move with stealing
  rather than with the resource (ablation observations) is consistent with
  this.
- **Done**: the `avg_min_need` and `need_deficit_rate` metrics were added.
- **Deprivation experiment (2026-10-09, 480 runs, shuffled order)**: while the
  store indicator is saturated at both levels, real deprivation lowers the
  `steal` share under the original score (well fed minus deprived +0.048
  [+0.045, +0.050]) and raises it under the need-based score (−0.034 [−0.037,
  −0.032]). Provisions reduce starvation deaths under deprivation. Under the
  need-based score, agents do not forage even when deprived because they
  believe the stores are empty, and the most starvation deaths are in those
  arms. Report: `DEPRIVATION_RESULTS.md`.
- **Proposed closure**: (a) in reports, make the distinction between "store
  emptiness" and "deprivation" instead of "scarcity", and report both together
  in every experiment; (b, started: `EXPERIMENT_PROTOCOL_DEPRIVATION.md`)
  define a resource regime that produces real deprivation (lowering
  regeneration below the need flow or removing the waste in foraging) —
  separate protocol; the default is not changed on the basis of this finding.
- **Status**: **open**.

### ISSUE-016 — Fixed agent order produces priority by agent ID under scarcity
- **Where**: `simulation/engine.py` (`step`, `agent_update_order="fixed"`)
- **What**: agents act in the same list order every tick, and the order is
  effective at the moment of foraging. When the stores do not meet the need,
  those at the head of the order get, and nothing is left for those at the
  end. Exploratory diagnostic (capacity 90, 4 seeds, seeds 92000–92003):

  | Regeneration | Order | Final population | Starvation deaths | Deaths among low-ID founders | Deaths among high-ID founders | Last-100 deprived share |
  |---|---|---:|---:|---:|---:|---:|
  | 0.004 | fixed | 25.0 | 64.2 | 0.14 | 1.00 | 0.045 |
  | 0.004 | shuffled | 51.8 | 31.0 | 0.25 | 0.33 | 0.247 |
  | 0.008 | fixed | 44.5 | 35.2 | 0.00 | 0.46 | 0.020 |
  | 0.008 | shuffled | 80.8 | 0.2 | 0.01 | 0.00 | 0.137 |

  Under the fixed order, all of the second half of the founders die of
  starvation; when the order is shuffled, death becomes independent of
  identity, total deaths halve, and lasting deprivation appears.
- **Consequence**: `SCHEDULE_ROBUSTNESS_RESULTS.md` and
  `AGENT_RNG_ROBUSTNESS_RESULTS.md` showed that the order does not change the
  results only in regimes where the agents are well fed; this robustness
  cannot be generalised to scarce regimes. There, the fixed order is an
  implicit "access hierarchy by agent ID" assumption. Since later-born agents
  have the highest identity, they access last.
- **Done**: the deprivation pilot was run with both orders
  (`output/deprivation_pilot*.json`); the deprivation experiment was defined
  with shuffled order (`EXPERIMENT_PROTOCOL_DEPRIVATION.md`).
- **Proposed closure**: explicitly report the order in every experiment that
  includes a scarce regime; decide whether the default should be `shuffled`
  (the `fixed` option must remain for the reproducibility of old
  experiments); verify the 4-seed diagnostic with n≥30.
- **Status**: **open**.

## Closed

### ISSUE-001 — The behavioural effect of misinformation_rate is weak [CLOSED — re-tested in the current model]
- **Where**: `configuration/config.py` (`misinformation_rate`), `cognition/decision.py`
- **History**: in the V2 period a consistent "misinformation ↑ →
  true_scarcity ↓" effect had been found in 6/8 seeds and was marked "partly
  closed".
- **Re-test (V6, with all layers active)**: the same comparison (n=60, 300
  ticks, 8 seeds) came out in the same direction in **4/8 seeds** in the
  current model — a coin flip, no longer a reliable effect. The other metrics
  (conflict_rate, cooperation_rate, inequality_gini, population) already
  showed no meaningful difference.
- **Interpretation**: after identity (V3), culture/norms (V3) and
  population/lifecycle (V4) were added, much stronger, dominant feedback loops
  (population boom/collapse, identity consolidation) formed in the system;
  these reduced the indirect effect of `misinformation_rate` to the noise
  level. The direct mechanical effect still stands (as misinformation_rate
  increases, the population-wide std of `scarcity_belief` rises slightly:
  0.074→0.078 in a single-seed test) but it no longer translates meaningfully
  into downstream behaviour.
- **Decision**: forcing the coefficients to obtain a stronger effect would be
  calibration to a desired result (contrary to PROJECT_CONSTITUTION rule 8).
  The current state was documented as is and closed.
- **Related task**: TASK-104
- **Status**: **closed**.

### ISSUE-002 — avg_trust is still low in absolute terms [FIXED — the root cause had been misidentified]
- **Where**: `sociology/social_network.py`
- **Symptom**: after TASK-101 (neighbourhood structure), `avg_trust` became
  additive but is still around ~0.03-0.05.
- ~~**Earlier (WRONG) hypothesis**: it was thought that `average_trust()` also
  counted never-interacting pairs as 0, diluting the mean.~~ **Measured, not
  correct**: the `self.trust[a]` dictionary gains a key only when `nudge()` is
  called (i.e. when there is a real interaction); `average_trust()` already
  averages only over interacting pairs. At n=80 after 300 ticks, 34% (2153) of
  the 6320 possible directed pairs had interacted, and the **own mean** of
  these 2153 pairs is ~0.037 — the low value comes from the real dynamics, not
  from dilution.
- **Real root cause**: positive (`socialize`/`share`, target ~0.3-0.7) and
  negative (`steal`, target -0.8) interactions largely cancel each other
  across the population (44% have |trust|<0.05), and on top of that
  `relationship_decay` continuously pulls edges that are not refreshed to
  zero. This is not a "dilution bug"; it may be a reasonable outcome of a
  mixed cooperation+betrayal environment.
- **Decision**: instead of artificially raising the number (PROJECT_CONSTITUTION
  rule 8: no "good society" goal), two new metrics showing the underlying
  distribution were added: `positive_relationship_rate`,
  `negative_relationship_rate`.
- **Related task**: TASK-104
- **Status**: **closed** — the root cause was corrected; it was not a "bug"
  but a missing measurable metric; resolved with the new metrics.

### ISSUE-003 — avg_institution_trust converges slowly to institution_legitimacy [CLOSED — root cause found and fixed]
- **Where**: `simulation/engine.py` (`_perceive_and_update_beliefs`), `cognition/beliefs.py`
- **Root cause found**: the noisy observation (`observed_legitimacy`) was
  clipped to [0,1] every tick BEFORE entering the blend. Since the true
  `legitimacy` is almost always very close to 0, this clipping lets only the
  positive half of the noise survive (a half-normal distribution) — which
  creates a systematic UPWARD bias (mathematically E[max(0,X)] ≈ 0.4×std,
  which almost exactly matches the observed ~0.08 deviation).
- **Fix**: the noisy observation is no longer clipped BEFORE entering the
  blend; only the FINAL `institution_trust` is clipped to [0,1] (this was
  already done inside `update_institution_trust`). The same pattern existed in
  the `scarcity_belief` observation; that was fixed too for consistency.
- **Verification** (3000 ticks, seed=42): after the fix, `avg_institution_trust`
  dropped from the ~0.08-0.15 band to the ~0.045-0.07 band — much closer to
  the true `legitimacy` (~0.01). The remaining small difference is a natural
  "reflecting boundary" effect arising from the belief being bounded to [0,1]
  and the true legitimacy being very close to zero — expected and reasonable.
- **Related task**: TASK-203
- **Status**: **closed**.

### ISSUE-004 — helping_norm keeps dropping toward ~0.30 [CLOSED — parameter screening done]
- **Where**: `culture/norms.py`, `cognition/decision.py`
- **Method**: we screened `identity_feedback_strength` over 0.0 (fully off) →
  0.1 → 0.15 → 0.3 (default) → 0.5, with n_agents=80/500 ticks/5 seeds, and
  measured with `summarize_window(window=50)`.

  | identity_feedback_strength | avg_trust | helping_norm | identity_formed_rate | positive_relationship_rate |
  |---|---|---|---|---|
  | 0.00 (off) | 0.011±0.002 | 0.303±0.004 | 1.000±0.000 | 0.212±0.012 |
  | 0.10 | 0.005±0.003 | 0.298±0.004 | 1.000±0.000 | 0.194±0.009 |
  | 0.15 | 0.004±0.002 | 0.295±0.005 | 1.000±0.000 | 0.197±0.009 |
  | 0.30 (default) | -0.007±0.003 | 0.268±0.009 | 1.000±0.000 | 0.166±0.008 |
  | 0.50 | -0.023±0.009 | 0.224±0.024 | 1.000±0.000 | 0.127±0.020 |

- **Result 1 (closes ISSUE-004)**: even at `identity_feedback_strength=0.0`
  (i.e. when identity has NO feedback on behaviour at all), `helping_norm`
  converges to the same ~0.30 level. So this is not a "self-feeding collapse"
  — `helping_norm` is merely correctly tracking the `cooperation_rate`
  equilibrium level (~0.25-0.35) that has existed since V1. It works as
  designed; no fix was needed.
- **Result 2 (verified finding)**: as `identity_feedback_strength` increases,
  `avg_trust` AND `positive_relationship_rate` decrease **monotonically** at
  all 5 levels, with narrow error margins. This confirms that TASK-302's claim
  "identity sunk cost erodes social trust" is a real, dose-dependent effect —
  not a bug, but a verified mechanism.
- **Related task**: TASK-301, TASK-302
- **Status**: **closed**.

### ISSUE-005 — there is no symmetric mechanism that repairs/reinforces trust [CLOSED — reconciliation mechanic added]
- **Where**: `simulation/engine.py` (`socialize` branch), `configuration/config.py` (`reconciliation_bonus`)
- **Solution**: in the `socialize` action, if the current trust is ALREADY
  negative (`social.get(...) < 0` — i.e. the relationship was previously
  damaged), the trust-nudge target is strengthened by `reconciliation_bonus`
  (default 0.35). That is, actively trying to repair a damaged relationship
  (by repeatedly `socialize`-ing) gives faster results than building an
  acquaintance from scratch — an active repair path that passive decay cannot
  provide.
- **Verification**: `test_reconciliation_repairs_damaged_trust_faster` — with
  n=2 agents, in a relationship manually set to -0.5 trust, a single
  `socialize` call was verified to produce a larger improvement than expected
  without the reconciliation bonus. In the default run (500 ticks)
  `avg_trust` improved from -0.047 to -0.035 — a modest but real effect (the
  erosion forces are still dominant; this is INTENTIONAL, see the verified
  finding of ISSUE-004).
- **Related task**: related to TASK-301/TASK-302, not numbered as a new subtask.
- **Status**: **closed**.

### ISSUE-006 — does true_scarcity really recover after 500 ticks [CLOSED — run to extinction]
- **Where**: `environment/ship.py`, `population/lifecycle.py`
- **Method**: the same default config was run with **2000** instead of n_ticks=500 (n=80, seed=42).
- **Finding — not the expected "recovery", but extinction**:

  | tick | population | true_scarcity | avg_stress | cumulative_births | cumulative_deaths_old_age |
  |---|---|---|---|---|---|
  | 1 | 80 | 0.328 | 0.220 | — | — |
  | 201 | 109 | 0.913 | 0.796 | (baby boom) | — |
  | 601 | 79 | 0.667 | 0.739 | — | — |
  | 801 | 54 | 0.012 | 0.380 | — | — |
  | 1201 | 15 | 0.007 | 0.356 | — | — |
  | 2000 | **1** | 0.000 | 0.126 | 33 (total) | **112** |

  `true_scarcity` really does drop at ~tick 800 — but it drops BECAUSE the
  population has collapsed, not because a healthy equilibrium has been
  reached. The population falls from 80 to 1. `cumulative_deaths_starvation=0`
  (final): nobody dies directly of starvation; after births stop, the
  population is exhausted one by one through old age.
- **Interpretation**: because ALL the founders are of reproductive age at the
  start, a one-off "baby boom" exceeds the carrying capacity, and there is no
  mechanism in the system to reverse it. Not a deliberate "bug" — the
  single-seed finding was confirmed multi-seed in ISSUE-007.
- **Related task**: TASK-401
- **Status**: **closed**.

### ISSUE-007 — multi-seed robustness of the population collapse [CLOSED — confirmed to be universal]
- **Where**: `population/lifecycle.py`, `environment/ship.py`, `experiments/counterfactual.py`
- **Method**: `run_v5_lab.py` — n=80, 2000 ticks, 3 conditions × 10 seeds:

  | Condition | ≤5 pop | ≤20 pop | below founders (80) |
  |---|---|---|---|
  | A) default config | 30% | 80% | **100%** |
  | B) `birth_rate_base` 0.008→0.003 (fewer births) | **100%** | 100% | 100% |
  | C) `resource_capacity_per_agent` 75→150 (2x resources) | **0%** | **0%** | 10% |

- **Result**: (A) the collapse is universal (10/10 seeds fall below the
  founding population). (B) the intuitive "fewer births helps" hypothesis
  turned out to be **wrong** — it makes things even worse. (C) it was
  confirmed that the real bottleneck is not the birth rate but **resource
  capacity**.
- **Decision**: the default config was DELIBERATELY NOT changed
  (PROJECT_CONSTITUTION rule 8) — anyone who wishes can run a stable scenario
  with an override such as `resource_capacity_per_agent=150` (see
  `run_v5_lab.py` condition C).
- **Related task**: TASK-501
- **Status**: **closed**.

### ISSUE-008 — has_leader==0 in causal_narrative fires meaninglessly at tick 1 [CLOSED]
- **Where**: `experiments/causal_narrative.py`
- **Symptom**: the "no leadership institution / disappeared" flag fired at
  tick 1 if a leader had NEVER formed — it did not distinguish "disappeared"
  from "never yet formed".
- **Fix**: leadership is now removed from the general threshold list and
  tracked with separate transition logic: only a real 1→0 transition is
  reported as "disappeared"; if it never formed, this is given as a separate,
  neutral informational note ("leadership never formed"), not as a warning
  flag.
- **Verification**: run on seed 0, n=80/500 ticks — there is now no
  meaningless "disappeared" line at tick 1; only the real warnings and the
  informational note at the end appear.
- **Related task**: TASK-502
- **Status**: **closed**.

### ISSUE-000 — the balance of true_scarcity broke when the population changed [CLOSED]
- **Symptom**: the regen/consumption balance calibrated for n_agents=80
  collapsed `true_scarcity`→0 at n_agents=60.
- **Solution**: resource capacity/initial stock were turned into `*_per_agent`
  config fields, and `Ship.__init__` multiplies them by `n_agents`.
- **Status**: **closed**.

### ISSUE-009 — random_acquaintance did O(n) filtering, causing superlinear behaviour at scale [CLOSED]
- **Where**: `sociology/social_network.py`
- **Finding method**: `run_scale_test.py` — wall-clock was measured from 100
  up to 10,000 agents. In the 100-1600 range the exponent was ≈1.05 (linear,
  no problem), but in the 1600-10,000 range it rose to ≈1.26 — a real
  superlinear behaviour.
- **Root cause isolation**: when `long_range_interaction_prob=0.0` was set, the
  exponent dropped from 1.26 to 1.04 — the culprit was definitely the
  long-range interaction fallback of `random_acquaintance` filtering the
  WHOLE population on every call with `[x for x in agent_ids if x != a]`
  (O(n) per call × n_agents calls/tick = O(n²)).
- **Fix**: switched to a reject-and-retry strategy (`rng.choice` + retry if
  equal, at most 5 attempts, falling back to the old filtering in pathological
  cases) — expected O(1).
- **Verification**: after the fix, the exponent in the 1600-10,000 range
  dropped from 1.26 to 1.09. At n=10,000 it is now ~0.35 s per tick (500
  ticks ≈ 3 minutes).
- **Related task**: scale test (post-V6 extension)
- **Status**: **closed**.


## Revalidation notes (n=30, formal test — details: REVALIDATION.md)
- **ISSUE-001** (misinformation ineffective): re-tested, **no significant
  effect in either regime**; the closure is now a statistically supported null
  result.
- **ISSUE-004** (identity erodes): only the endpoints (0.0 vs 0.5) were
  re-tested, and the direction was confirmed; the intermediate doses / the
  "monotonic" claim were not re-tested.
- **ISSUE-005** (reconciliation): the single-seed claim held at n=30 (−0.051 →
  −0.034), but the effect is only in `avg_trust`; conflict/inequality/
  population do not change.
