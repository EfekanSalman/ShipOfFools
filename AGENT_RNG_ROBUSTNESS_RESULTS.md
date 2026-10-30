# Update Order Robustness with Per-Agent RNG

## Research question

Did updating actions in fixed ID order change the effects of resource capacity and
regeneration? In the earlier robustness analysis the agents' actions shared a single
decision RNG. For this reason, when the update order changed, the number of random
draws consumed by one agent could shift the draws going to subsequent agents. In
this follow-up the action/lifecycle draws were separated into per-agent streams.

## Design

- 2×2 resource layout: capacity 90/120, food and water regeneration rate 0.016/0.019.
- In each cell the same 30 seeds were run with both the fixed and the per-tick
  shuffled action order: 4 cells × 30 seeds × 2 schedules = 240 simulations.
- Each run contains 80 founder agents and 500 ticks; the analysis is the within-seed
  mean of the last 100 ticks.
- `agent_rng_mode="per_agent"` uses an RNG derived from the agent ID for action
  decisions, perception noise, interaction target, rumor distortion, being caught,
  aging and birth draws. The per-tick ordering uses a separate scheduler RNG.
- 10,000 paired bootstrap resamples were made for the matched-seed differences within
  a cell and for the factorial contrast differences.

This separates the transfer of RNG draws across agents; it is not a full
common-random-numbers/potential-outcomes design. When an agent's action and
interactions change, that agent's subsequent draw count/path may also change. The
environment, network initialization and leader media draws continue to use the main
simulation RNG. Within these runs each seed/schedule is reproducible; the per-agent
mode does not change the `shared` default.

## Primary factorial results

Contrast is high level minus low level; Δ is the shuffled action order minus fixed
order contrast. The brackets are the paired seed bootstrap 95% interval for Δ.

| Outcome / contrast | Fixed | Shuffled | Δ (95% CI) |
|---|---:|---:|---:|
| Cooperation — capacity | +0.096 | +0.093 | −0.003 [−0.009, +0.003] |
| Cooperation — regeneration | +0.042 | +0.041 | −0.001 [−0.007, +0.006] |
| Cooperation — interaction | +0.024 | +0.021 | −0.004 [−0.016, +0.009] |
| Conflict — capacity | −0.105 | −0.102 | +0.004 [−0.003, +0.011] |
| Conflict — regeneration | −0.042 | −0.043 | −0.001 [−0.008, +0.006] |
| Conflict — interaction | −0.020 | −0.017 | +0.003 [−0.011, +0.017] |
| Scarcity — capacity | −0.560 | −0.554 | +0.006 [−0.041, +0.052] |
| Scarcity — regeneration | −0.231 | −0.228 | +0.003 [−0.043, +0.049] |
| Scarcity — interaction | −0.176 | −0.190 | −0.014 [−0.107, +0.078] |

All nine difference intervals contain zero, and the capacity/regeneration main
effects of the three outcomes are in the same direction in both schedules. This
analysis does not prove the equivalence of the update orders; there is no
pre-specified equivalence bound, and the between-seed variability widens the
intervals especially in the scarcity/interaction estimates. Nevertheless, the earlier
resource result kept its direction in a design that is less dependent on the shift of
RNG draws across agents.

## Next methodological decision

The `shared` mode was kept as the default so that old experiments remain repeatable
unchanged. In new research, whether `per_agent` mode should become the default should
be chosen by evaluating together the replication of the core findings under `shared`
and `per_agent` and the methodological rationale of the per-agent stream design.
Counter-based RNG, which pins common exogenous events by agent ID/tick, could be a
future alternative for stronger matching.

## Scope note (2026-10-09)

This result belongs to the resource cells in which the agents were well fed; in
scarce regimes the update order changes the results (ISSUE-016).

## Reproduction

- `run_agent_rng_robustness.py` — 240 runs and the raw time series.
- `analyze_agent_rng_robustness.py` — paired cell and factorial bootstrap analysis.
- `output/agent_rng_robustness/experiment.json` — design/seed metadata.
- `output/agent_rng_robustness/analysis.json` — result estimates and intervals.
- `output/agent_rng_robustness/seed_summaries.csv` — 240 seed/schedule summaries.
- `output/agent_rng_robustness/timeseries.csv` — 120,000 tick observations.
