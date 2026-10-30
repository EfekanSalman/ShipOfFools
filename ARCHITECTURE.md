# Architecture

This document describes the current code. Research assumptions and the
scientific limits of the model are kept in [REFERENCES.md](REFERENCES.md) and
[KNOWN_ISSUES.md](KNOWN_ISSUES.md). When a new mechanism is added, this
document and [TASK_GRAPH.md](TASK_GRAPH.md) must be updated.

## Layers

```text
configuration/config.py
        │
environment/ship.py ── physical resource pool and environmental events
        │
economy/resources.py ── shared resources, forage and wealth
        │
agents/agent.py ── personality, needs, memory, identity, metacognition
        ├── cognition/beliefs.py, decision.py, mental_models.py
        ├── sociology/social_network.py ── trust graph and small-world neighbourhood
        ├── information/rumors.py ── rumour and belief transmission
        ├── institutions/ ── leadership, law enforcement, education, health, media
        ├── culture/norms.py ── help and authority norms
        └── population/lifecycle.py ── ageing, death and birth
        │
simulation/engine.py ── main simulation loop that connects the layers
        ├── metrics/ ── population, economy and network measures
        ├── experiments/ ── multi-seed, statistics, counterfactual and sensitivity
        └── visualization/ ── PNG plots and HTML dashboard data
```

`Config` is the single source of simulation parameters. The scarcity-belief
terms in the `share`/`steal` scores also live there
(`steal_scarcity_weight`, `share_scarcity_weight`,
`action_scarcity_reference`; ISSUE-013); the other coefficients in the
decision formula are still fixed inside `cognition/decision.py`.

`decision_architecture` selects between two decision architectures. The
default `"heuristic"` is the original scoring. `"need_based"` (ISSUE-014)
changes two things: wealth becomes edible provisions (inside
`_update_internal_state`, while the need is below `provision_eat_threshold`),
and the `forage`/`steal`/`share` scores are computed from the agent's need
urgency × the action's yield for that need, instead of directly from the
scarcity-belief coefficient. The tick order and RNG draws do not change. The
two parts can be switched on separately for factorial experiments:
`provisions_edible` and `need_based_scoring` (when `None`, they follow
`decision_architecture`). In the default `shared` RNG mode, random model
operations are run through `Simulation.rng`. In the experimental `per_agent`
mode, agent actions and per-agent lifecycle draws are taken from streams
seeded with fixed agent IDs; random operations in environment, media and
network setup still use the simulation stream. Tick scheduling can also be
chosen as `fixed` or `shuffled`. The dashboard export uses a separate RNG.

## Tick flow

`Simulation.step()` roughly follows this order on each tick:

1. The environment and resource pool are updated; the trust of social ties
   decays.
2. Leadership is updated, and norms are updated with observations from the
   previous tick.
3. Each living agent perceives the environment with noise, updates its beliefs
   and self-assessment, and then selects an action via the utility/softmax
   decision mechanism.
4. Actions change resources, trust relations, rumours and institutional
   interactions; the agent's internal state and identity are updated.
5. Ageing, death, education and birth processes are run; if present, the
   public reserve is distributed.
6. Metrics are recorded.

The exact order in the implementation may change; when mechanics change, this
section must be updated together with `simulation/engine.py`.

## Implemented mechanisms

- **Cognition:** noisy perception of scarcity and legitimacy, belief updating,
  memory, self-assessment and a partial second-order mental model.
- **Social structure:** small-world local neighbourhood, long-range
  interactions, trust/relationship updates and rumour transmission.
- **Economy and institutions:** resource foraging and sharing, theft,
  leadership, taxation/redistribution, law enforcement, education, health
  recovery and partial media broadcast.
- **Culture and population:** help and authority norms; identity from repeated
  behaviour; ageing, death, birth and family transmission of
  personality/beliefs.
- **Research tools:** metrics tracker, multi-seed and matched counterfactual
  runs, Morris-type screening, a limited 2x2 interaction analysis, statistical
  summaries and visualisation.

The existence of these mechanisms does not mean that their empirical validity
has been demonstrated. For the evidence level of the parameters and mechanism
assumptions, see `REFERENCES.md`.

## Deliberate scope limits

- **Missing institutions:** religious and scientific institutions are not
  modelled. Law enforcement, education, health and media are simple
  approximations; the societal effects of the institutions are not
  empirically calibrated.
- **Economy:** there are no prices, labour market, unemployment or
  multiple-occupation system; forage specialisation is a simple learning
  effect.
- **Culture:** the norm system consists of two simple axes; language/jargon
  evolution and a broad cultural space are not modelled.
- **Cognition:** fully nested theory of mind and predictive processing/active
  inference are not implemented (TASK-602b).
- **Experimental design:** the Morris-type screening does not measure
  parameter interactions; there is a 2x2 experiment only for two specific
  parameters. The scarcity ceiling effect in the default regime and some
  small-sample findings are open research limitations (ISSUE-011/012).
- **Scale:** `run_scale_test.py` measures runtime on short runs; it does not
  verify that long-run results are equivalent across population sizes.
- **Dashboard:** this is a first version showing sample agents and the
  last-tick network. It does not work offline because of CDN dependencies;
  visual verification in a real browser is the open ISSUE-010.

## Resource capacity design

`environment/ship.py` computes resource capacity from the founding population
(`config.n_agents`). If the population grows through births, capacity does not
grow automatically; this is an assumption chosen in order to study
carrying-capacity pressure. This choice depends on the research question and
must be stated when interpreting results.
