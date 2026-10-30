# Scarcity Belief → Action Score Ablation — Results

## Status and level of interpretation

**Run completed: 2026-10-07.** The protocol
(`EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`) was written before the run and
was not changed during it. This is an in-model, theoretical/exploratory
analysis; it is neither a calibration to human data nor an empirical
validation.

## Method (summary)

- 2×2 resource (capacity 90/120; food+water regeneration 0.016/0.019) × 3 link
  arms = 12 cells; 30 seed blocks (60000–60029) per cell; 360 simulations.
- Arms: `intact` (default); `zero` (`steal_scarcity_weight` and
  `share_scarcity_weight` = 0); `fixed` (`action_scarcity_reference=0.5`).
- 80 founder agents, 500 ticks, fixed order, `agent_rng_mode="shared"`. The last
  100 ticks were averaged within each seed; the seed is the unit of analysis.
- Square brackets are 10,000-draw seed-block bootstrap 95% intervals. There are
  no p-values or multiple-comparison corrections.

## Primary results

Contrast = high level minus low level. Retained fraction = arm contrast /
`intact` contrast.

| Outcome / contrast | `intact` | `zero` | `fixed` | Retained fraction `zero` | Retained fraction `fixed` |
|---|---:|---:|---:|---:|---:|
| Conflict — capacity | −0.101 [−0.108, −0.093] | +0.012 [+0.011, +0.014] | +0.014 [+0.012, +0.016] | −0.12 [−0.14, −0.11] | −0.14 [−0.17, −0.11] |
| Conflict — regeneration | −0.042 [−0.047, −0.037] | +0.004 [+0.003, +0.005] | +0.008 [+0.005, +0.010] | −0.09 [−0.13, −0.06] | −0.18 [−0.25, −0.12] |
| Conflict — interaction | −0.033 [−0.046, −0.021] | +0.002 [−0.002, +0.006] | −0.011 [−0.014, −0.007] | — | — |
| Cooperation — capacity | +0.095 [+0.087, +0.102] | +0.023 [+0.021, +0.026] | +0.013 [+0.011, +0.015] | +0.25 [+0.21, +0.28] | +0.14 [+0.11, +0.16] |
| Cooperation — regeneration | +0.044 [+0.039, +0.049] | +0.008 [+0.005, +0.010] | +0.007 [+0.004, +0.009] | +0.18 [+0.12, +0.24] | +0.15 [+0.10, +0.20] |
| Cooperation — interaction | +0.033 [+0.022, +0.044] | +0.007 [+0.002, +0.012] | −0.008 [−0.012, −0.004] | — | — |

The `intact` arm reproduced the first resource experiment, which used different
seeds (the conflict capacity effect there was −0.099, here −0.101; cooperation
+0.090 and +0.095).

According to the interpretation rules written in advance:

- **Conflict measure:** in both ablation arms the capacity and regeneration
  contrasts exclude zero and their signs are the **opposite** of those in the
  `intact` arm. When the direct term is cut, the favourable resource condition
  does not reduce the `steal` share; it increases it slightly (by roughly one
  eighth of the magnitude). As the rule requires: the indirect channels work
  against the direct term; the `intact` result reflects the dominance of the
  direct term.
- **Cooperation measure:** the contrasts exclude zero and the sign is the same;
  14–25% of the effect is independent of the direct term. The remainder comes
  mostly from the `socialize` share (below).

The two ablation arms give the same result in the main effects; they differ only
in the interaction terms (see the level note below).

## Manipulation check

| Outcome / contrast | `intact` | `zero` | `fixed` |
|---|---:|---:|---:|
| True scarcity — capacity | −0.562 [−0.609, −0.513] | −0.461 [−0.519, −0.404] | −0.655 [−0.700, −0.610] |
| True scarcity — regeneration | −0.234 [−0.266, −0.203] | −0.243 [−0.279, −0.206] | −0.302 [−0.348, −0.256] |
| Scarcity belief — capacity | −0.510 [−0.559, −0.459] | −0.405 [−0.458, −0.354] | −0.587 [−0.628, −0.548] |
| Scarcity belief — regeneration | −0.218 [−0.248, −0.188] | −0.227 [−0.261, −0.193] | −0.262 [−0.302, −0.222] |

In all three arms the resource manipulation continues to change true scarcity and
the agents' scarcity belief; the primary contrasts can be interpreted. The
ablation cut not the belief but only the belief's entry into the `share`/`steal`
scores.

## Cell means

Columns: 90/0.016, 90/0.019, 120/0.016, 120/0.019.

| Measure | Arm | 90/0.016 | 90/0.019 | 120/0.016 | 120/0.019 |
|---|---|---:|---:|---:|---:|
| `steal` share (conflict) | `intact` | 0.321 | 0.295 | 0.237 | 0.178 |
| | `zero` | 0.120 | 0.123 | 0.132 | 0.136 |
| | `fixed` | 0.218 | 0.231 | 0.238 | 0.240 |
| `share` share | `intact` | 0.083 | 0.103 | 0.141 | 0.192 |
| | `zero` | 0.217 | 0.219 | 0.228 | 0.235 |
| | `fixed` | 0.128 | 0.134 | 0.137 | 0.139 |
| `socialize` share | `intact` | 0.088 | 0.096 | 0.109 | 0.118 |
| | `zero` | 0.109 | 0.111 | 0.118 | 0.122 |
| | `fixed` | 0.101 | 0.105 | 0.108 | 0.109 |
| `forage` share | `intact` | 0.163 | 0.154 | 0.161 | 0.169 |
| | `zero` | 0.207 | 0.195 | 0.171 | 0.168 |
| | `fixed` | 0.184 | 0.170 | 0.170 | 0.170 |
| True scarcity | `intact` | 0.982 | 0.880 | 0.552 | 0.186 |
| | `zero` | 1.000 | 0.991 | 0.773 | 0.296 |
| | `fixed` | 0.978 | 0.504 | 0.151 | 0.022 |
| Stress | `intact` | 0.843 | 0.783 | 0.652 | 0.516 |
| | `zero` | 0.422 | 0.417 | 0.394 | 0.399 |
| | `fixed` | 0.704 | 0.700 | 0.710 | 0.706 |
| Mean trust | `intact` | −0.035 | −0.017 | 0.001 | 0.017 |
| | `zero` | 0.035 | 0.034 | 0.034 | 0.035 |
| | `fixed` | −0.013 | −0.014 | −0.013 | −0.013 |
| Population | `intact` | 93.4 | 107.0 | 113.3 | 118.8 |
| | `zero` | 108.9 | 126.3 | 129.0 | 129.0 |
| | `fixed` | 92.1 | 93.5 | 94.8 | 93.2 |
| `benefactor` label share | `intact` | 0.079 | 0.278 | 0.384 | 0.480 |
| | `zero` | 0.663 | 0.658 | 0.667 | 0.665 |
| | `fixed` | 0.121 | 0.119 | 0.121 | 0.126 |

## Secondary exploratory results

Capacity contrast (high minus low):

| Measure | `intact` | `zero` | `fixed` |
|---|---:|---:|---:|
| Stress | −0.229 [−0.247, −0.212] | −0.023 [−0.032, −0.013] | +0.006 [−0.002, +0.015] |
| Mean trust | +0.035 [+0.033, +0.037] | −0.000 [−0.001, +0.001] | +0.000 [−0.001, +0.001] |
| `helping_norm` | +0.096 [+0.090, +0.103] | +0.024 [+0.022, +0.026] | +0.012 [+0.010, +0.014] |
| `benefactor` label share | +0.254 [+0.234, +0.273] | +0.005 [−0.008, +0.018] | +0.004 [−0.006, +0.014] |
| `opportunist` label share | −0.112 [−0.123, −0.100] | +0.012 [+0.002, +0.021] | −0.003 [−0.017, +0.011] |
| `forage` share | +0.006 [+0.002, +0.010] | −0.032 [−0.035, −0.028] | −0.007 [−0.010, −0.004] |
| `share` share | +0.073 [+0.067, +0.080] | +0.013 [+0.011, +0.016] | +0.007 [+0.005, +0.008] |
| `socialize` share | +0.021 [+0.020, +0.023] | +0.010 [+0.009, +0.011] | +0.006 [+0.005, +0.007] |
| Gini | +0.013 [+0.005, +0.021] | −0.028 [−0.037, −0.020] | −0.006 [−0.014, +0.003] |
| Population | +15.9 [+13.5, +18.3] | +11.3 [+8.8, +13.9] | +1.2 [−0.4, +2.9] |

Observations (exploratory; mechanism explanations are untested candidates):

- **Downstream effects are also tied to the same term.** The effects of the
  resource regime on trust, stress, helping norm, and the composition of identity
  labels either disappear in the ablation arms or fall to one tenth. In the
  `intact` arm these effects are not separate findings; they are consequences of
  the direct term in the `steal`/`share` scores.
- **Stress tracks stealing more than it tracks the absence of resources.** In
  the `fixed` arm, true scarcity falls from 0.98 to 0.02 while stress stays
  constant at 0.70; the `steal` share is also constant in that arm (~0.23). In
  the `zero` arm the `steal` share is low (~0.13) and stress is low (~0.40),
  even when scarcity is high. In the engine, a victim of stealing directly
  receives +0.2 stress; this is the candidate explanation.
- **Population appears to move with stress, not with resource abundance.** In the
  `fixed` arm, population stays at 93 in the most abundant cell where scarcity is
  0.02 (`intact` 119). A birth requires the mother's stress to be below 0.6, and
  mean stress in this arm is 0.70. Candidate explanation: in this model, what
  limits population growth is stress from stealing, not the amount of resources.
- **Candidate for the reversed sign: the `forage` squeeze.** In the ablation
  arms the `forage` share falls under the favourable condition (`zero` −0.032),
  and the freed share is distributed among the other actions; `steal` takes a
  share of it as well. This was one of the two directions anticipated in the
  protocol.

## Limits of interpretation

- **Level difference.** The `zero` arm lowers the `steal` score overall (share
  ~0.13), while the `fixed` arm roughly preserves it (~0.23). Although the two
  arms give the same result in the main effects, their interaction terms differ;
  in the `fixed` arm the most abundant cell sticks to the scarcity floor (0.02),
  and in the `zero` arm the scarcest cell sticks to the ceiling (1.00). The
  interaction contrasts should therefore not be compared across arms.
- The ablation also changes the scarcity level (less scarcity in the `fixed`
  arm, more in the `zero` arm); the arms are not a "different decision rule at
  the same scarcity" comparison.
- The 0.5 in the `fixed` arm is a researcher's choice; another constant would
  give a different level.
- Only the term in the `share`/`steal` scores was cut. The `scarcity_belief`
  term in the `spread_belief` score and the perceptual bias from stress remain in
  place.
- The seed bootstrap summarises seed uncertainty; it does not cover mechanism and
  parameter uncertainty. The same seed label is not a full common-random-numbers
  design.

## Conclusion and reporting decision

The H2 result in `RESOURCE_STRESS_RESULTS.md` ("favourable resource condition →
less conflict, more cooperation") is, in this model, a consequence of two
coefficients in `decision.py`. It should not be presented as an emergent finding;
it should be reported as a verification result, namely that "the scarcity
sensitivity written into the decision rule shows up at the population level in
the expected direction". Without the direct term, the effect of the resource
regime on the conflict measure is small and in the opposite direction.

The default coefficients were not changed in light of this result (principle 9).

## Reproduction files

- Protocol: `EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`.
- Run: `run_scarcity_link_ablation.py`; analysis: `analyze_scarcity_link_ablation.py`.
- `output/scarcity_link_ablation/experiment.json` — design and seed metadata.
- `output/scarcity_link_ablation/analysis.json` — cell means, contrasts, arm
  differences, and retained fractions for all measures.
- `output/scarcity_link_ablation/seed_summaries.csv` — 360 seed/cell summaries.
- `output/scarcity_link_ablation/timeseries.csv` — 180,000 tick observations.
