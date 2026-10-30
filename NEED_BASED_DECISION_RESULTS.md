# Need-Based Decision Architecture × Resource Regime — Results

## Status and level of interpretation

**Run completed: 2026-10-09.** The protocol
(`EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`) was written before the run on
2026-10-07 and was not changed. The first run was cut off at 50 of 240 worlds
when the session closed; it had produced no summary or analysis file and its
results were not examined. The experiment was re-run from scratch with the same
seeds. This is an in-model, theoretical/exploratory analysis.

## Method (summary)

- 2×2 resource (capacity 90/120; food+water regeneration 0.016/0.019) × 2
  architectures (`intact` = default heuristic; `need_based`) = 8 cells; 30 seed
  blocks (70000–70029) per cell; 240 simulations.
- 80 founder agents, 500 ticks, fixed order, `agent_rng_mode="shared"`. The last
  100 ticks were averaged within each seed; the seed is the unit of analysis.
- Square brackets are 10,000-draw seed-block bootstrap 95% intervals. There are
  no p-values or multiple-comparison corrections.

## Primary results

Contrast = high level minus low level. Ratio = `need_based` / `intact`.

| Outcome / contrast | `intact` | `need_based` | Ratio |
|---|---:|---:|---:|
| Conflict — capacity | −0.098 [−0.105, −0.090] | −0.012 [−0.013, −0.010] | 0.12 [0.10, 0.14] |
| Conflict — regeneration | −0.042 [−0.047, −0.038] | −0.007 [−0.008, −0.005] | 0.15 [0.12, 0.19] |
| Conflict — interaction | −0.024 [−0.040, −0.009] | +0.008 [+0.004, +0.011] | — |
| Cooperation — capacity | +0.092 [+0.084, +0.099] | +0.016 [+0.014, +0.018] | 0.17 [0.15, 0.20] |
| Cooperation — regeneration | +0.045 [+0.040, +0.050] | +0.008 [+0.006, +0.010] | 0.18 [0.13, 0.23] |
| Cooperation — interaction | +0.024 [+0.011, +0.036] | −0.009 [−0.014, −0.005] | — |

According to the rule written in advance: in the `need_based` arm, all four
main-effect contrasts exclude zero and their signs are the same as in `intact`.
**The relationship also emerges through the need channel, without a direct
coefficient; but its magnitude is between about one eighth and one sixth of that
in the `intact` arm.** The expectation in the protocol was confirmed as far as
the sign is concerned. The rule's own record applies: this does not prove that
the relationship is "emergent"; it shows that it also derives from a weaker
assumption in the decision rule.

The `intact` arm gave the same result in a third independent seed block (conflict
capacity effect −0.099, −0.101, −0.098).

The interaction terms have opposite signs in the two arms; in the `need_based`
arm the resource factors head toward saturation instead of reinforcing each
other.

## Manipulation check

| Outcome / contrast | `intact` | `need_based` |
|---|---:|---:|
| True scarcity — capacity | −0.560 [−0.611, −0.507] | −0.527 [−0.563, −0.490] |
| True scarcity — regeneration | −0.250 [−0.283, −0.217] | −0.265 [−0.306, −0.222] |
| Scarcity belief — capacity | −0.508 [−0.560, −0.456] | −0.498 [−0.532, −0.465] |
| Scarcity belief — regeneration | −0.226 [−0.256, −0.195] | −0.243 [−0.279, −0.205] |

The resource manipulation produces a scarcity difference of similar size in both
arms; the primary contrasts can be interpreted.

## Cell means

| Measure | Arm | 90/0.016 | 90/0.019 | 120/0.016 | 120/0.019 |
|---|---|---:|---:|---:|---:|
| `steal` share (conflict) | `intact` | 0.319 | 0.289 | 0.234 | 0.179 |
| | `need_based` | 0.192 | 0.181 | 0.176 | 0.173 |
| `share` share | `intact` | 0.084 | 0.108 | 0.143 | 0.191 |
| | `need_based` | 0.168 | 0.180 | 0.186 | 0.190 |
| `forage` share | `intact` | 0.162 | 0.154 | 0.161 | 0.170 |
| | `need_based` | 0.126 | 0.139 | 0.153 | 0.168 |
| True scarcity | `intact` | 0.992 | 0.837 | 0.527 | 0.182 |
| | `need_based` | 0.898 | 0.644 | 0.383 | 0.106 |
| Stress | `intact` | 0.844 | 0.765 | 0.657 | 0.522 |
| | `need_based` | 0.583 | 0.549 | 0.528 | 0.520 |
| Mean wealth | `intact` | 60.9 | 56.2 | 49.7 | 49.1 |
| | `need_based` | 38.6 | 44.9 | 46.5 | 48.4 |
| Gini | `intact` | 0.416 | 0.409 | 0.420 | 0.433 |
| | `need_based` | 0.448 | 0.441 | 0.428 | 0.421 |
| Population | `intact` | 94.3 | 106.9 | 115.7 | 117.8 |
| | `need_based` | 110.8 | 114.1 | 116.1 | 115.7 |

In the most abundant cell (120/0.019) the two architectures give almost the same
behaviour shares; the divergence grows as scarcity increases.

## Secondary exploratory results

Capacity contrast (high minus low):

| Measure | `intact` | `need_based` |
|---|---:|---:|
| Mean wealth | −9.1 [−10.3, −7.9] | +5.8 [+4.6, +6.9] |
| Gini | +0.015 [+0.007, +0.022] | −0.020 [−0.027, −0.013] |
| `forage` share | +0.007 [+0.005, +0.010] | +0.028 [+0.026, +0.030] |
| `share` share | +0.071 [+0.065, +0.078] | +0.014 [+0.012, +0.016] |
| `socialize` share | +0.020 [+0.018, +0.022] | +0.002 [+0.001, +0.003] |
| `spread_belief` share | −0.016 [−0.019, −0.013] | −0.039 [−0.042, −0.037] |
| Stress | −0.215 [−0.231, −0.200] | −0.042 [−0.051, −0.033] |
| Mean trust | +0.034 [+0.032, +0.035] | +0.003 [+0.002, +0.004] |
| Population | +16.2 [+13.1, +19.2] | +3.4 [+0.9, +6.0] |
| `benefactor` label share | +0.234 [+0.215, +0.253] | +0.018 [+0.001, +0.035] |

> **Correction (2026-10-09).** The explanation in the first two observations
> below ("because wealth is eaten") was not supported by the subsequent
> decomposition experiment: the sign change is also seen in the `scoring_only`
> arm, where wealth cannot be eaten, and belongs mostly to the score form. See
> `PROVISION_SCORING_FACTORIAL_RESULTS.md`. The numbers stand; the
> interpretation has changed.

Observations (exploratory; mechanism explanations are untested candidates):

- **Wealth moves in opposite directions in the two architectures.** In the
  `intact` arm the scarcest cell is the richest cell (60.9 versus 49.1): wealth
  accumulates because it is of no use. In the `need_based` arm, wealth decreases
  under scarcity (38.6 versus 48.4), because it is eaten. This is how ISSUE-014
  shows up in the data.
- **The response of Gini to the resource regime changes sign.** In the `intact`
  arm, abundance slightly increased Gini (the unexpected finding in the first
  resource experiment); in the `need_based` arm, abundance lowers Gini. The first
  finding appears to depend on wealth being a number that cannot be eaten;
  inferences about Gini are sensitive to the architecture.
- **Population is more resilient to scarcity.** In the scarcest cell, population
  is 111 instead of 94. Possible causes: provisions acting as a need buffer, and
  lower stress with a lower `steal` share (0.58 versus 0.84). This is consistent
  with the ablation's candidate that "stress from stealing limits population",
  but this experiment does not separate them.
- **The `forage` share freed under scarcity goes mostly to `spread_belief`, not
  to `steal`.** The stress and `scarcity_belief` terms in the `spread_belief`
  score are still in place in this architecture.
- Between-seed variability for the conflict measure is very small in the
  `need_based` arm (SD 0.006; 0.012–0.029 in the `intact` arm).

## Reading the three experiments together

Capacity effect on the conflict measure (separate seed blocks; the arms should
not be differenced directly):

| Decision rule | Capacity effect | Source |
|---|---:|---|
| Direct scarcity-belief term (default) | −0.098 to −0.101 | three experiments |
| No term (`zero`) | +0.012 | ablation |
| Fixed term (`fixed`) | +0.014 | ablation |
| Need-based, edible provisions | −0.012 | this experiment |

The **direction** of the resource regime → conflict relationship is the same in
two of the decision rules and reversed in the third; its **magnitude** varies by
roughly a factor of eight depending on the decision rule. No magnitude claim of
the form "scarcity increases conflict by this much" can be drawn from this model.
The defensible claim is the structural uncertainty itself: the result is
determined not by resource dynamics but by the individual decision-rule
assumption.

## Limits of interpretation

- The `need_based` arm also adds eating provisions; the two arms do not operate
  at the same scarcity level (scarcity is somewhat lower in every cell of this
  arm). The comparison is of the "decision rule + provisions" package; the two
  were not separated.
- The reason the effect turned out small was not tested. Candidates: because mean
  wealth is 39–48, agents' provisions rarely run out and urgency is suppressed;
  the payoff from a theft (`g = 0.4`) is low relative to foraging.
- Sensitivity to `provision_max_per_tick` and the other `provision_*` values was
  not tested. They were not changed in light of this result (principle 9);
  sensitivity requires a separate protocol and a new seed block.
- Mass conservation in foraging is not complete (protocol, Limits).
- The seed bootstrap summarises seed uncertainty; the table above shows
  precisely the model uncertainty that it does not cover.

## Reproduction files

- Protocol: `EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`.
- The run and analysis commands are in the "Implementation" section of the
  protocol.
- `output/need_based_decision/experiment.json`, `analysis.json`,
  `seed_summaries.csv` (240 rows); `timeseries.csv` (120,000 tick observations,
  outside git).
