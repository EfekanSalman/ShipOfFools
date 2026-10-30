# Protocol: Edible Provisions × Need-Based Scoring × Resource Regime

**Status:** the protocol was written before the run (2026-10-09). The results are
reported in the separate file `PROVISION_SCORING_FACTORIAL_RESULTS.md`.

## Question

In `NEED_BASED_DECISION_RESULTS.md` the `need_based` arm changed two things at once:
wealth being edible, and the `forage`/`steal`/`share` scores being computed by need
urgency × payoff. Which of these two parts does the change in the effect of the
resource regime on the conflict and cooperation measures belong to, and are they
dependent on each other?

## Design

- Resource factors are the same as before: capacity 90/120; food and water
  regeneration 0.016/0.019; initial stock 2/3 of capacity.
- On the decision side a 2×2, four arms:

  | Arm | Edible provisions | Need-based scoring | `Config` |
  |---|---|---|---|
  | `intact` | no | no | default |
  | `provisions_only` | yes | no | `provisions_edible=True` |
  | `scoring_only` | no | yes | `need_based_scoring=True` |
  | `need_based` | yes | yes | `decision_architecture="need_based"` |

- 2×2×4 = 16 cells; 30 seed blocks (80000–80029) in each cell; 480 simulations.
  The seed range had not been used before. The same seed label is not a full
  common-random-numbers design.
- 80 founder agents, 500 ticks, fixed order, `agent_rng_mode="shared"`. The last 100
  ticks are averaged within each seed; the seed is the unit of analysis.
- The `provision_*` values are the same as in the previous experiment and are not changed.

The meaning of the two intermediate arms:

- `provisions_only`: the original scores (including the direct `scarcity_belief`
  terms) are kept; when agents go hungry they eat from their wealth.
- `scoring_only`: scores are computed by urgency × payoff but wealth cannot be eaten.
  In this arm the payoff term in the `steal` score assumes a gain that has no
  counterpart in the engine; the agent's valuation is in effect wrong. The arm exists
  to separate the effect of the score form from the provision dynamics.

## Measures and analysis

**Primary:** the main effects of capacity and regeneration for `conflict_rate` and
`cooperation_rate`, in each arm; and the 2×2 decomposition of these contrasts on the
decision side:

- provisions main effect = ((`provisions_only` − `intact`) + (`need_based` −
  `scoring_only`)) / 2,
- scoring main effect = ((`scoring_only` − `intact`) + (`need_based` −
  `provisions_only`)) / 2,
- provisions × scoring interaction = (`need_based` − `scoring_only`) −
  (`provisions_only` − `intact`).

**Manipulation check:** `true_scarcity`, `avg_scarcity_belief`.

**Secondary (exploratory):** action shares, `avg_stress`, `avg_trust`,
`inequality_gini`, `avg_wealth`, `population`, `helping_norm`, identity label
shares.

Uncertainty: 10,000-draw seed-block bootstrap, 95% percentile interval.
No p-value or multiple-comparison correction; all cells are reported.

## What was known before the run, and expectation

The `intact` and `need_based` arms were run before in different seed blocks (conflict
capacity effect ≈ −0.10 and −0.012 respectively); they are re-run in this experiment.
The `provisions_only` and `scoring_only` arms were never run.

Expectation (weak):

- Most of the difference in the conflict measure belongs to the **scoring** factor,
  because it is the one that removes the direct term; in the ablation, when the term
  was removed, the effect had gone from −0.10 to +0.012.
- In the `provisions_only` arm the capacity effect stays close to `intact`; it may
  shrink somewhat because provisions buffer needs.
- The difference between `scoring_only` and `need_based`, i.e. the effect of
  provisions when scoring is on, is uncertain in sign. Without provisions, theft does
  not relieve need and urgency stays high; this may raise the `steal` share in every
  cell and enlarge or flatten the resource contrast.

## Interpretation rules

- If the interval of a main effect in the decomposition excludes zero, that factor
  changes the resource effect; if it covers zero, it is not distinguishable in this
  sample.
- If the interaction interval excludes zero, the two parts cannot be interpreted
  independently of each other; the separate contrasts of the four arms, rather than
  the main effects, are taken as the basis.
- If the contrasts of the `intact` and `need_based` arms in this experiment are not in
  the same direction and of similar magnitude as in the earlier experiments, this is
  reported separately.
- The primary contrasts of an arm whose manipulation check does not pass are not
  interpreted.
- The `provision_*` values or the score terms are not changed by looking at the
  result (principle 9).

## Limits

Same as in the previous protocol: the arms do not operate at the same scarcity level;
mass conservation in foraging is not exact; there is no calibration with external data.

## Implementation

```
py run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based \
   --seed-start 80000 --out-dir output/provision_scoring_factorial \
   --protocol EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md
py analyze_scarcity_link_ablation.py --dir output/provision_scoring_factorial \
   --factorial provisions_only,scoring_only,need_based
```
