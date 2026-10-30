# PROJECT CONSTITUTION — Ship of Fools

This project is developed through AI orchestration: research, architecture,
coding and review proceed in different "roles" (see doc 4). This file defines
the fixed rules that all of those roles must follow. Before a new feature is
added, it must first be checked against these rules.

1. **Emergence > scripting.** Behaviour must arise from the interaction of
   personality + needs + stress + beliefs; it must not be forced by fixed
   "if X then do Y" rules.
2. **No fixed labels.** No agent is written into the code as "foolish",
   "smart", "good" or "bad". Derived metrics such as `Agent.foolishness` are
   time-dependent states, not identities.
3. **Reality ≠ the agent's belief.** Every agent must have its own (possibly
   wrong) world model; no agent accesses global state directly, and each
   receives only noisy/biased observations via `_perceive_and_update_beliefs`.
4. **Scientific claims must be documented.** Every mechanism inspired by
   neuroscience/psychology must state: (a) which phenomenon it represents,
   (b) why it was included, (c) which simplification was made, (d) the limits
   of that simplification. This project does not claim to be a biologically
   accurate model of the brain.
5. **ML is not forced everywhere.** If simple methods such as utility/softmax
   suffice, no deep learning is added (V0 `cognition/decision.py` is an
   example).
6. **Reproducibility is mandatory.** The same code, configuration and seed
   must produce the same model trajectory. The random-stream design must be
   explicitly documented: by default the shared `Simulation.rng`, or
   experimental per-agent streams. Auxiliary random work outside the model,
   such as metric sampling, must use a separate, documented seed/stream and
   must not consume the simulation's RNG sequence.
7. **Do not trust a single run.** Experimental results (`experiments/runner.py`)
   must be reported as a distribution (mean/std) over multiple seeds; the
   result of a single run does not count as "evidence". Starting two different
   configurations with the same seed does not by itself provide common random
   numbers / a matched experiment: different branches of the conditions can
   bring the RNG draws out of alignment. The RNG design used must be
   explained and verified before matched inference (`ODD_D.md`,
   `ACADEMIC_RESEARCH_PLAN.md`).
8. **No "good society" goal.** The system does not mark any configuration as
   "best"; it only reports measurable metrics such as stability, cooperation,
   inequality and trust. Value judgements are left to the user.
9. **Every subsystem is tested.** When a new mechanism is added, at least one
   sanity test must be added under `tests/`.
10. **Architectural decisions are documented.** When a new layer/mechanism is
    added, `ARCHITECTURE.md` and `TASK_GRAPH.md` must be updated.
