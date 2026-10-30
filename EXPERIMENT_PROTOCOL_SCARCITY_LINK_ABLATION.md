# Protocol: Ablation of the Scarcity Belief → Action Score Link

**Status:** the protocol was written before the run (2026-10-07). The results are
reported in the separate file `SCARCITY_LINK_ABLATION_RESULTS.md`.

## Question

To what extent does the "favorable resource condition → less `steal`, more
`share`/`socialize`" result in the resource experiment
(`RESOURCE_STRESS_RESULTS.md`) come from the direct terms in the decision formula?

## Rationale

In `cognition/decision.py` the `steal` score contains `+0.9 × scarcity_belief` and
the `share` score contains `−0.5 × scarcity_belief`. `scarcity_belief` is a noisy
reading of true scarcity; `conflict_rate` is the share of agents whose final action
is `steal`. Therefore the H2 result is, at least in part, the read-back of a
relationship hand-written into the formula (ISSUE-013). This experiment cuts the
direct link and measures how much of the resource effect remains through the indirect
channels (needs, stress, norms, identity, population). It falls under principle 7
and Stage 5 of `ACADEMIC_RESEARCH_PLAN.md`. It is a within-model, theoretical/exploratory
analysis.

## Design

- Resource factors are the same as in the earlier experiments: capacity 90/120; food
  and water regeneration together 0.016/0.019; initial stock 2/3 of capacity.
- Link factor, three arms:
  - `intact` — default (`steal_scarcity_weight=0.9`,
    `share_scarcity_weight=0.5`).
  - `zero` — both weights 0. The direct term is removed entirely; the overall level
    of the `steal` score falls, that of the `share` score rises.
  - `fixed` — `action_scarcity_reference=0.5`. The `share`/`steal` scores read a
    fixed 0.5 instead of the agent's belief; the weights stay in place, so the score
    level is roughly preserved but the change depending on the resource condition is
    cut. 0.5 is the midpoint of the scale and is a researcher's choice.
- The two ablation arms are reported together; one is not chosen in place of the
  other. Since softmax is nonlinear, the contrasts may depend on the score level; the
  divergence of the two arms is an indicator of this dependence.
- The ablation cuts only the term in the `share` and `steal` scores. The
  `+0.3 × scarcity_belief` in the `spread_belief` score, the belief itself,
  `needs.safety` and the stress bias do not change.
- 2×2×3 = 12 cells; 30 seeds per cell; 360 simulations in total. The same 30 seeds
  (60000–60029) are used in all cells (seed-blocked). This seed range had not been
  used before. The same seed label is not a full common-random-numbers design.
- 80 founder agents, 500 ticks; fixed agent order; `agent_rng_mode="shared"` (for
  comparability with the earlier resource experiments).
- Unit: one seed/cell simulation. Metrics are averaged per seed within the last 100
  ticks. Ticks are not counted as independent samples.

## Measures

**Primary:** `conflict_rate` and `cooperation_rate`.

**Manipulation check:** `true_scarcity` and `avg_scarcity_belief`. The resource
manipulation must continue to change scarcity in every arm; if it does not, the
primary contrasts of that arm are not interpreted.

**Secondary (exploratory):** the separate shares of the six actions
(`action_*_rate`), `avg_stress`, `avg_trust`, `inequality_gini`, `population`,
`helping_norm`, the four identity label shares. The action shares are there to show
which one rises when an action falls.

## Analysis

- Within each arm, the capacity main effect, the regeneration main effect and the
  capacity × regeneration interaction (high minus low), from seed-level summaries.
- For each ablation arm, the contrast difference: arm minus `intact`.
- For the capacity and regeneration main effects in the primary measures, the
  **retained fraction**: arm contrast / `intact` contrast.
- Uncertainty: 10,000-draw seed-block bootstrap, 95% percentile interval, recorded
  analysis seed. No p-value or multiple-comparison correction; all cells and all
  primary contrasts are reported.

## Interpretation rules written in advance

No prediction is made about the direction of the remaining effect. The indirect
channels can work in both directions: under scarcity needs fall, the `forage` score
rises and within softmax can squeeze out both the `steal` and the `share` shares; on
the other hand, stress and norm feedback can work in favor of `steal`.

- If the within-arm contrast interval covers zero: there is no effect distinguishable
  from the indirect channels in this sample. It is not settled as "no effect".
- If the interval excludes zero and the sign is the same as `intact`: part of the
  effect is independent of the direct term; its magnitude is given by the retained
  fraction.
- If the interval excludes zero and the sign is reversed: the indirect channels work
  opposite to the direct term; the `intact` result reflects the dominance of the
  direct term.
- Whatever the result, the default coefficients are not changed by looking at this
  experiment (principle 9).

## Stopping and reporting

30 seeds/cell is determined in advance; after the run starts, the sample, measures or
arms are not changed by looking at the results. The outputs are written to
`output/scarcity_link_ablation/`: `experiment.json`, `seed_summaries.csv`,
`timeseries.csv`, `analysis.json`. Scripts: `run_scarcity_link_ablation.py`,
`analyze_scarcity_link_ablation.py`.
