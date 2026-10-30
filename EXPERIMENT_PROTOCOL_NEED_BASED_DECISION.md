# Protocol: Need-Based Decision Architecture × Resource Regime

**Status:** the protocol was written before the run (2026-10-07). The results are
reported in the separate file `NEED_BASED_DECISION_RESULTS.md`.

## Question

When the scarcity belief is not written directly into the `steal`/`share` scores, but
wealth is edible provisions and actions are scored by their effect on the agent's own
need, does the resource regime change the conflict and cooperation measures?

## Rationale

The ablation (`SCARCITY_LINK_ABLATION_RESULTS.md`) showed that the effect of the
resource regime on the conflict measure depends on the direct term in `decision.py`
(ISSUE-013). Beneath this there is a structural gap (ISSUE-014): wealth satisfies no
need, i.e. stealing cannot relieve hunger. This experiment establishes that link and
tests whether the relationship emerges without a coefficient.

## Mechanism (`decision_architecture="need_based"`)

The default (`"heuristic"`) does not change and preserves the old trajectories bit for bit.

1. **Wealth = provisions.** If an agent's food or water need is below
   `provision_eat_threshold` (0.4), that tick it eats at most
   `provision_max_per_tick` (1.0) wealth; each unit raises both needs by
   `provision_need_per_wealth` (0.1).
2. **Outcome-based score.** The direct `scarcity_belief` terms in the `steal` and
   `share` scores are removed. In their place, with the urgency
   `u = 1.2(1−food) + 1.2(1−water)` (the term in the existing `forage` score):
   - `forage` −= `u × scarcity_belief` (if the agent thinks the stores are empty,
     foraging pays less),
   - `steal` += `u × g`, `share` −= `u × g`.
   `g` is the ratio of the provisions a theft yields to one basic foraging and is
   derived from existing constants: `(2.0 × 0.1) / (forage_base_amount / 10) = 0.4`.

Parameter grounds: the 0.1 ratio is the ratio the engine already uses for sharing
with a child (2.0 wealth → +0.2 food and water). The 0.4 threshold is the level at
which scarcity pressure begins in the stress formula. The 1.0 upper limit is a new
design choice and its sensitivity has not been tested.

The scores are still hand-written. The difference is this: the assumption becomes
"the agent weighs an action by its payoff to its own need" instead of "the scarcity
belief increases stealing"; the scarcity → stealing direction does not appear in the
formula.

## Design

- Resource factors are the same as before: capacity 90/120; food and water
  regeneration 0.016/0.019; initial stock 2/3 of capacity.
- Architecture factor, two arms: `intact` (heuristic, default) and `need_based`.
- 2×2×2 = 8 cells; 30 seed blocks (70000–70029) in each cell; 240 simulations.
  The seed range had not been used before. The same seed label is not a full
  common-random-numbers design.
- 80 founder agents, 500 ticks, fixed order, `agent_rng_mode="shared"`. The last 100
  ticks are averaged within each seed; the seed is the unit of analysis.

The only `need_based` output seen before the run is a smoke test made with seed 42
in the default configuration (it is not one of the experiment cells and seeds).

## Measures and analysis

**Primary:** within the `need_based` arm, the main effects of capacity and
regeneration and the interaction for `conflict_rate` and `cooperation_rate`.

**Manipulation check:** `true_scarcity`, `avg_scarcity_belief`.

**Secondary (exploratory):** action shares, `avg_stress`, `avg_trust`,
`inequality_gini`, `avg_wealth`, `population`, `helping_norm`, identity label
shares; `need_based` minus `intact` contrast differences and ratios.

Uncertainty: 10,000-draw seed-block bootstrap, 95% percentile interval.
No p-value or multiple-comparison correction; all cells are reported.

## Expectation written in advance and interpretation rules

Expectation: under an unfavorable resource condition foraging pays less, needs fall,
urgency rises; this should raise the `steal` share and lower the `share` share. That
is, in the `need_based` arm too, a negative capacity effect for conflict and a
positive one for cooperation are expected. Channels that could break the expectation:
there being nothing left to steal in a population whose provisions are exhausted, the
`forage` share squeezing out the other actions, the eaten provisions protecting needs
and suppressing urgency.

- If in the `need_based` arm the contrast excludes zero and the sign is the same as
  in `intact`: the relationship emerges from the need channel as well, without a
  direct coefficient. This does not prove that the relationship is "emergent"; it
  shows that it derives from a weaker assumption in the decision rule.
- If the interval covers zero: there is no distinguishable effect in this sample.
- If the sign is reversed: under the need-based rule resource abundance increases
  stealing; the mechanism is examined through the action shares.
- If the manipulation check does not pass in the `need_based` arm, the primary
  contrasts are not interpreted.
- The `provision_*` parameters or the score terms are not changed by looking at the
  result (principle 9). If a change is needed, a new protocol and a new seed block.

## Limits

- The `need_based` arm also adds eating provisions; the two arms do not operate at
  the same scarcity level. The comparison is of the "decision rule + provisions"
  package.
- The wealth gained in foraging is written in addition to the need gain (the
  engine's current state); when it can be eaten as provisions, this means additional
  nutrition of about 10% of the foraging yield. Mass conservation is not exact.
- There is no calibration with external data; interpretations are within the model.

## Implementation

```
py run_scarcity_link_ablation.py --arms intact,need_based --seed-start 70000 \
   --out-dir output/need_based_decision --protocol EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md
py analyze_scarcity_link_ablation.py --dir output/need_based_decision
```
