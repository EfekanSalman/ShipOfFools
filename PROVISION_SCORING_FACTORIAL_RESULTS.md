# Edible Provisions × Need-Based Score × Resource Regime — Results

## Status and level of interpretation

**Run completed: 2026-10-09.** The protocol
(`EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`) was written and
committed (`a29ff7f`) before the run. The first attempt was stopped without
writing the summary file because system memory ran short; its results were not
examined and the experiment was re-run from scratch with the same seeds. This
is an in-model, theoretical/exploratory analysis.

## Method (summary)

- 2×2 resource (capacity 90/120; regeneration 0.016/0.019) × 4 decision arms =
  16 cells; 30 seed blocks (80000–80029) per cell; 480 simulations.
- Arms: `intact`; `provisions_only` (wealth is edible, scores original);
  `scoring_only` (scores need-based, wealth not edible); `need_based` (both at
  once).
- 80 founder agents, 500 ticks, fixed order, `agent_rng_mode="shared"`. The last
  100 ticks were averaged within each seed. Square brackets are 10,000-draw
  seed-block bootstrap 95% intervals.

## Primary results

Capacity and regeneration main effects (high minus low), within arm:

| Outcome / contrast | `intact` | `provisions_only` | `scoring_only` | `need_based` |
|---|---:|---:|---:|---:|
| Conflict — capacity | −0.097 [−0.104, −0.089] | −0.096 [−0.103, −0.088] | −0.016 [−0.018, −0.014] | −0.011 [−0.013, −0.010] |
| Conflict — regeneration | −0.045 [−0.051, −0.039] | −0.045 [−0.050, −0.040] | −0.007 [−0.009, −0.006] | −0.005 [−0.007, −0.003] |
| Cooperation — capacity | +0.090 [+0.084, +0.096] | +0.091 [+0.084, +0.097] | +0.019 [+0.017, +0.021] | +0.018 [+0.015, +0.020] |
| Cooperation — regeneration | +0.046 [+0.040, +0.051] | +0.045 [+0.039, +0.050] | +0.009 [+0.007, +0.011] | +0.009 [+0.006, +0.011] |

The 2×2 decomposition of these contrasts on the decision side:

| Outcome / contrast | Provisions main effect | Scoring main effect | Provisions × scoring |
|---|---:|---:|---:|
| Conflict — capacity | +0.003 [−0.002, +0.007] | +0.082 [+0.076, +0.089] | +0.004 [−0.004, +0.012] |
| Conflict — regeneration | +0.001 [−0.003, +0.005] | +0.039 [+0.035, +0.043] | +0.002 [−0.007, +0.010] |
| Cooperation — capacity | −0.000 [−0.004, +0.004] | −0.072 [−0.077, −0.067] | −0.001 [−0.009, +0.006] |
| Cooperation — regeneration | −0.001 [−0.005, +0.004] | −0.036 [−0.041, −0.032] | +0.001 [−0.007, +0.010] |

According to the rules written in advance:

- The **scoring factor** changes the resource effect: in all four contrasts the
  interval excludes zero. Nearly all of the difference between `intact` and
  `need_based` belongs to the score form.
- The **provisions factor** cannot be distinguished in this sample: in all four
  contrasts the interval includes zero and the point estimates are smaller than
  one twentieth of the scoring effect.
- The **interaction** intervals include zero; the two components can be
  interpreted separately.

The expectation in the protocol (most of the difference belongs to scoring) was
confirmed. The expectation that the `provisions_only` arm would stay close to
`intact` also held; the anticipated shrinkage was not seen. The effect of
provisions when scoring is on (the sign of which had been called uncertain) is
small and its interval touches zero.

Replications: `intact` is −0.097 in the fourth independent seed block (earlier
ones −0.099, −0.101, −0.098); `need_based` is −0.011 in the second block
(previously −0.012).

## Manipulation check

The true scarcity capacity contrast is between −0.51 and −0.55 in the four arms,
and the regeneration contrast between −0.25 and −0.28; all of the intervals
exclude zero. In the decomposition, the effects of the provisions and scoring
factors on the scarcity contrast include zero. The primary contrasts can be
interpreted.

## Cell means

| Measure | Arm | 90/0.016 | 90/0.019 | 120/0.016 | 120/0.019 |
|---|---|---:|---:|---:|---:|
| `steal` share | `intact` | 0.321 | 0.291 | 0.239 | 0.179 |
| | `provisions_only` | 0.322 | 0.291 | 0.240 | 0.181 |
| | `scoring_only` | 0.195 | 0.184 | 0.176 | 0.172 |
| | `need_based` | 0.190 | 0.182 | 0.176 | 0.173 |
| `share` share | `intact` | 0.082 | 0.105 | 0.138 | 0.186 |
| | `provisions_only` | 0.081 | 0.103 | 0.138 | 0.187 |
| | `scoring_only` | 0.166 | 0.177 | 0.185 | 0.189 |
| | `need_based` | 0.164 | 0.176 | 0.184 | 0.189 |
| True scarcity | `intact` | 0.997 | 0.849 | 0.553 | 0.192 |
| | `provisions_only` | 0.992 | 0.858 | 0.561 | 0.197 |
| | `scoring_only` | 0.923 | 0.692 | 0.455 | 0.133 |
| | `need_based` | 0.949 | 0.696 | 0.420 | 0.143 |
| Stress | `intact` | 0.849 | 0.777 | 0.668 | 0.525 |
| | `provisions_only` | 0.832 | 0.775 | 0.661 | 0.524 |
| | `scoring_only` | 0.625 | 0.561 | 0.534 | 0.517 |
| | `need_based` | 0.576 | 0.553 | 0.526 | 0.522 |
| Mean wealth | `intact` | 62.0 | 57.3 | 51.6 | 49.0 |
| | `provisions_only` | 58.9 | 55.8 | 51.7 | 48.8 |
| | `scoring_only` | 41.6 | 45.9 | 46.8 | 48.8 |
| | `need_based` | 37.1 | 44.0 | 46.3 | 48.4 |
| Gini | `intact` | 0.420 | 0.407 | 0.412 | 0.435 |
| | `provisions_only` | 0.435 | 0.413 | 0.418 | 0.431 |
| | `scoring_only` | 0.447 | 0.441 | 0.437 | 0.421 |
| | `need_based` | 0.457 | 0.441 | 0.434 | 0.429 |
| Population | `intact` | 93.0 | 106.4 | 113.2 | 118.9 |
| | `provisions_only` | 95.2 | 107.6 | 114.4 | 119.1 |
| | `scoring_only` | 111.7 | 116.5 | 119.7 | 117.1 |
| | `need_based` | 114.9 | 116.5 | 117.8 | 118.2 |

## Secondary exploratory results

Decomposition of the capacity contrast:

| Measure | Provisions main effect | Scoring main effect |
|---|---:|---:|
| Mean wealth | +2.5 [+1.6, +3.4] | +13.6 [+12.5, +14.8] |
| Gini | −0.006 [−0.015, +0.002] | −0.021 [−0.030, −0.014] |
| Stress | +0.017 [+0.004, +0.029] | +0.159 [+0.144, +0.175] |
| Population | −1.5 [−3.6, +0.6] | −12.5 [−15.3, −9.6] |
| Mean trust | −0.001 [−0.002, +0.000] | −0.030 [−0.031, −0.028] |
| `forage` share | −0.001 [−0.002, +0.001] | +0.023 [+0.021, +0.025] |

**Correction to the previous report.** In `NEED_BASED_DECISION_RESULTS.md` I had
interpreted the sign change in the response of wealth and Gini to the resource
regime as "because wealth is eaten", and had counted this as the form in which
ISSUE-014 shows up in the data. This experiment does not support that
interpretation: the sign change is also present in the `scoring_only` arm, where
wealth cannot be eaten (wealth capacity effect +4.0), and absent in the
`provisions_only` arm, where wealth is eaten but scores stay original (−7.1).
The change belongs mostly to the score form; the share of provisions is small
for wealth (+2.5) and indistinguishable for Gini. The population's resilience to
scarcity also belongs to scoring. A correction note was added to that report.

## Why are provisions ineffective? (exploratory diagnosis)

A small diagnostic run outside the protocol (two extreme resource cells × 3 arms
× 5 seeds, seeds 90000–90004, last 100 ticks; with the new `avg_min_need` and
`need_deficit_rate` metrics):

| Cell | Arm | True scarcity | Mean lowest need | Share with need below 0.4 |
|---|---|---:|---:|---:|
| 90/0.016 | `intact` | 0.998 | 0.798 | 0.039 |
| 90/0.016 | `provisions_only` | 0.967 | 0.806 | 0.019 |
| 90/0.016 | `scoring_only` | 0.862 | 0.769 | 0.075 |
| 120/0.019 | `intact` | 0.157 | 0.861 | 0.002 |
| 120/0.019 | `provisions_only` | 0.205 | 0.859 | 0.001 |
| 120/0.019 | `scoring_only` | 0.066 | 0.855 | 0.004 |

In the cell where true scarcity is at the ceiling (≈1.0), agents' mean lowest
need is 0.80 and only 4% are below the 0.4 threshold. Agents are well fed even
at "maximum scarcity"; provisions are not eaten because the hunger that would
trigger eating rarely arises.

The reason for this is the definition of the measure: `true_scarcity = 1 −
stock/capacity` (`economy/resources.py`), that is, it measures how full the
stores are, not deprivation. A rough calculation with the default values:
capacity 90 × 80 = 7200 and with regeneration 0.016 about 115 units of food
arrive each tick; since need decay is 0.03/tick and the foraging yield of 10
units = 1.0 need, about 30 units suffice to feed 100 agents. The flow is several
times the need. The stores are depleted all the same, because one foraging
action takes 5–12 units and need is clipped at 1.0; the excess is lost. This is
consistent with the observation in ISSUE-006 that "nobody dies of starvation".
Details and consequences are in ISSUE-015.

This diagnosis is an exploratory look at 5 seeds; the calculation is derived
from the code.

## Conclusion

1. The shrinking of the resource → conflict relationship by the `need_based`
   architecture comes from the score form; whether wealth is edible does not
   change behaviour in this model.
2. That wealth satisfies no need (ISSUE-014) is structurally correct, but its
   practical importance is lower than assumed: agents do not go hungry anyway.
3. The real issue is one level up: "scarcity" in the model is a stores indicator,
   and the only way it affects agents' behaviour is through the belief about
   this indicator. All of the resource experiments answer the question "what do
   agents do when they think the stores are empty", not "what do agents do when
   they go hungry".

## Limits of interpretation

- The limits in the previous protocol apply: arms do not operate at the same
  scarcity level; mass conservation in foraging is not complete; there is no
  calibration to external data.
- The ineffectiveness of provisions may be specific to the value
  `provision_eat_threshold=0.4`; a higher threshold was not tested.
- The seed bootstrap summarises seed uncertainty; it does not cover model
  uncertainty.

## Reproduction files

- Protocol and commands: `EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`.
- `output/provision_scoring_factorial/experiment.json`, `analysis.json`
  (the `arm_factorial` key contains the decomposition), `seed_summaries.csv`
  (480 rows); `timeseries.csv` is outside git.
