# True Deprivation × Decision Architecture — Results

## Status and level of interpretation

**Run completed: 2026-10-09.** The protocol (`EXPERIMENT_PROTOCOL_DEPRIVATION.md`)
was written and committed (`d0c9bda`) before the run. This is an
in-model, theoretical/exploratory analysis; there is no calibration to human
data.

## Method (summary)

- Capacity 90/120 × regeneration 0.004 (deprived) / 0.010 (empty stores, agents
  largely well fed) × four decision arms = 16 cells; 30 seed blocks
  (94000–94029); 480 simulations.
- `agent_update_order="shuffled"` (ISSUE-016). 80 founder agents, 500 ticks,
  `agent_rng_mode="shared"`. The last 100 ticks were averaged within each seed.
- Regeneration contrast = 0.010 minus 0.004 = **well fed minus deprived**. A
  positive value indicates that the measure is higher in the well-fed
  condition.
- Square brackets are 10,000-draw seed-block bootstrap 95% intervals.

## Manipulation check

| Measure | `intact` | `provisions_only` | `scoring_only` | `need_based` |
|---|---:|---:|---:|---:|
| Deprived share — regeneration contrast | −0.206 [−0.213, −0.199] | −0.214 [−0.223, −0.205] | −0.077 [−0.087, −0.068] | −0.236 [−0.243, −0.228] |
| True scarcity — cell means | 1.000 | 0.998–1.000 | 0.991–1.000 | 0.984–1.000 |
| Scarcity belief — cell means | 0.990–0.991 | 0.982–0.990 | 0.982–0.986 | 0.976–0.985 |

The deprivation manipulation passed in all four arms; the stores indicator and
the belief about it are saturated in every cell. The behavioural difference
between the two regeneration levels cannot come directly from the
`scarcity_belief` terms. The contrast is smaller in the `scoring_only` arm
because the "well-fed" level of that arm is also 13–19% deprived.

## Primary results

Regeneration contrast (well fed minus deprived):

| Outcome | `intact` | `provisions_only` | `scoring_only` | `need_based` |
|---|---:|---:|---:|---:|
| Conflict (`steal` share) | +0.048 [+0.045, +0.050] | +0.051 [+0.047, +0.054] | −0.006 [−0.009, −0.003] | −0.034 [−0.037, −0.032] |
| Cooperation | +0.015 [+0.014, +0.017] | +0.020 [+0.018, +0.022] | −0.009 [−0.012, −0.006] | +0.020 [+0.017, +0.023] |

Provisions × scoring decomposition of the conflict contrast: provisions main
effect −0.012 [−0.015, −0.010], scoring main effect −0.069 [−0.073, −0.066],
interaction −0.031 [−0.038, −0.025]. Because the interaction excludes zero, the
separate contrasts of the four arms are used instead of the main effects, as the
rule requires.

According to the rule written in advance: **in the two arms with original
scores, deprivation lowers the `steal` share (by 4.8–5.1 points); in the two
arms with need-based scores, it raises it (by 0.6 and 3.4 points); all four
intervals exclude zero. The direction of the effect of true deprivation on the
conflict measure depends on the decision-rule assumption.**

Comparison with expectations:

| Expectation | Result |
|---|---|
| Original scores: `steal` lower under deprivation | Confirmed (+0.048, +0.051) |
| Original scores: cooperation lower under deprivation | Confirmed (+0.015, +0.020) |
| Need-based scores: `steal` higher under deprivation | Confirmed (−0.006, −0.034); very small in `scoring_only` |
| Need-based scores: cooperation lower under deprivation | Confirmed in `need_based` (+0.020); **did not hold in `scoring_only`** (−0.009: cooperation is higher under deprivation) |
| More starvation deaths in the need-based arms | Confirmed (below) |
| Provisions lower the deprived share; primary effect small but larger than before | Partly: its effect on the primary contrast can now be distinguished and it interacts with scoring; the deprived share changes in two directions depending on capacity (below) |

## Cell means

Columns: 90/0.004, 90/0.010, 120/0.004, 120/0.010.

| Measure | Arm | 90 deprived | 90 well fed | 120 deprived | 120 well fed |
|---|---|---:|---:|---:|---:|
| `steal` share | `intact` | 0.268 | 0.318 | 0.280 | 0.325 |
| | `provisions_only` | 0.259 | 0.321 | 0.291 | 0.331 |
| | `scoring_only` | 0.218 | 0.219 | 0.219 | 0.206 |
| | `need_based` | 0.230 | 0.215 | 0.252 | 0.198 |
| `forage` share | `intact` | 0.260 | 0.187 | 0.255 | 0.166 |
| | `provisions_only` | 0.295 | 0.181 | 0.239 | 0.163 |
| | `scoring_only` | 0.124 | 0.121 | 0.123 | 0.120 |
| | `need_based` | 0.139 | 0.123 | 0.127 | 0.123 |
| Deprived share | `intact` | 0.253 | 0.070 | 0.257 | 0.027 |
| | `provisions_only` | 0.319 | 0.027 | 0.146 | 0.011 |
| | `scoring_only` | 0.236 | 0.185 | 0.236 | 0.133 |
| | `need_based` | 0.259 | 0.067 | 0.321 | 0.042 |
| Starvation deaths (total) | `intact` | 29.0 | 0.0 | 9.4 | 0.0 |
| | `provisions_only` | 12.7 | 0.0 | 0.0 | 0.0 |
| | `scoring_only` | 60.1 | 12.4 | 45.6 | 1.8 |
| | `need_based` | 48.0 | 0.0 | 13.8 | 0.0 |
| Population | `intact` | 56.0 | 86.1 | 74.7 | 90.6 |
| | `provisions_only` | 73.9 | 86.4 | 84.6 | 89.4 |
| | `scoring_only` | 42.6 | 90.7 | 58.3 | 103.3 |
| | `need_based` | 56.7 | 103.9 | 86.3 | 107.7 |
| Mean wealth | `intact` | 38.0 | 49.2 | 37.8 | 59.3 |
| | `provisions_only` | 1.0 | 42.6 | 7.0 | 57.5 |
| | `scoring_only` | 27.3 | 32.2 | 27.4 | 39.5 |
| | `need_based` | 1.5 | 19.3 | 1.2 | 32.7 |
| Stress | `intact` | 0.795 | 0.847 | 0.848 | 0.846 |
| | `provisions_only` | 0.545 | 0.837 | 0.770 | 0.846 |
| | `scoring_only` | 0.578 | 0.699 | 0.626 | 0.674 |
| | `need_based` | 0.415 | 0.653 | 0.560 | 0.608 |

## Secondary exploratory results

Mechanism explanations are untested candidates.

- **Under original scores, deprivation pushes agents toward foraging.** In the
  `intact` arm the `forage` share is 0.26 in the deprived condition and
  0.17–0.19 in the well-fed condition; the share it frees up comes from `steal`
  and `spread_belief`. This is the squeeze anticipated in the protocol.
- **Under need-based scores, agents do not forage even when deprived.** The
  `forage` share is constant at 0.12–0.14 across the four cells. The score
  multiplies the return on foraging by the belief about the stores; when the
  belief is ≈1, the urgency term is zeroed out. Result: the most starvation
  deaths occur in these arms (`scoring_only` 60 and 46; `intact` 29 and 9).
  **This is a design weakness of the mechanism:** even when the stores indicator
  is empty, there is a flow regenerating every tick and an agent that forages
  receives a share of it; the agent's belief that "the stores are empty, so
  foraging is pointless" is in effect wrong. The score form was not changed in
  light of this result (principle 9); a fix requires a separate protocol.
- **Provisions work under deprivation.** With original scores, starvation deaths
  go from 29 to 13 (capacity 90) and from 9.4 to 0.03 (capacity 120); in the
  deprived cells wealth is almost entirely eaten (38 → 1). The ineffectiveness
  in the well-fed regimes was because starvation did not occur (ISSUE-015); this
  experiment confirms that.
- **In the provisions arms the deprived share does not change in a single
  direction** (0.25 → 0.32 at capacity 90, 0.26 → 0.15 at 120). A possible cause
  is survival selection: agents who would die without provisions stay alive and
  deprived. The measure is computed over living agents.
- **Stress falls when wealth is exhausted.** In the `provisions_only` 90/deprived
  cell, stress is 0.55 (`intact` 0.80), while the `steal` share is similar
  (0.26). In the engine, theft takes place only if the victim's wealth exceeds 1
  and adds stress to the victim; when wealth is ≈1, attempts may be coming to
  nothing. This is consistent with the "stress tracks stealing" candidate from the
  ablation.
- The effect of capacity on the primary measures is small (absolute value ≤ 0.021).

## Reading together with the resource experiments

| Condition | Decision rule | Effect of the adverse condition on the `steal` share |
|---|---|---|
| Stores are being depleted, agents well fed (fixed order) | original | increases (≈ +0.10) |
| | term cut | slightly decreases (≈ −0.012) |
| | need-based | slightly increases (≈ +0.012) |
| Stores already empty, agents deprived (shuffled order) | original | decreases (≈ −0.048) |
| | need-based | increases (≈ +0.034) |

Under the original decision rule, the result that "scarcity increases conflict"
appears only through the belief channel and while agents are well fed; when
agents are truly deprived, the same rule gives the opposite. The robust
conclusion that can be drawn from the model is not a sign or a magnitude but
this: the scarcity → conflict relationship depends on (a) whether scarcity is a
belief or deprivation and (b) the decision rule.

## Limits of interpretation

- Population differs greatly across cells (43–108); the shares are computed over
  living agents and those who die of starvation drop out of the measurement
  (survival selection).
- The "well-fed" level is not fully well fed (deprived share 0.01–0.19,
  depending on the arm).
- Earlier experiments were run with fixed order and this one with shuffled
  order; the table above puts the two designs side by side and should not be
  differenced directly.
- The second rule, which chose the comparison level, was written after the pilot
  had been seen.
- The `provision_*` values and score terms were not tested/changed; mass
  conservation in foraging is not complete; there is no calibration to external
  data.

## Reproduction files

- Protocol and commands: `EXPERIMENT_PROTOCOL_DEPRIVATION.md`.
- Pilot: `run_deprivation_pilot.py`, `output/deprivation_pilot.json` (fixed
  order), `output/deprivation_pilot_shuffled.json`.
- `output/deprivation/experiment.json`, `analysis.json`, `seed_summaries.csv`
  (480 rows); `timeseries.csv` is outside git.
