# Next Steps

Last updated: 2026-10-30. This file is a short working plan; detailed history is
in [TASK_GRAPH.md](TASK_GRAPH.md) and open issues are in
[KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Main result so far

In this model, the sign of the scarcity → conflict relationship depends on two
things: whether scarcity is a belief or real deprivation, and the decision rule.

| Condition | Decision rule | Effect of the adverse condition on the `steal` share |
|---|---|---|
| Stores are being depleted, agents well fed (fixed order) | original | increases (≈ +0.10) |
| | direct term cut | slightly decreases (≈ −0.012) |
| | need-based | slightly increases (≈ +0.012) |
| Stores already empty, agents deprived (shuffled order) | original | decreases (≈ −0.048) |
| | need-based | increases (≈ +0.034) |

The two designs use different update orders; the table is for side-by-side
reading and the values should not be differenced directly. The results are
internal to the model and make no claim about real societies. Reports:
[SCARCITY_LINK_ABLATION_RESULTS.md](SCARCITY_LINK_ABLATION_RESULTS.md),
[NEED_BASED_DECISION_RESULTS.md](NEED_BASED_DECISION_RESULTS.md),
[PROVISION_SCORING_FACTORIAL_RESULTS.md](PROVISION_SCORING_FACTORIAL_RESULTS.md),
[DEPRIVATION_RESULTS.md](DEPRIVATION_RESULTS.md).

## Upcoming work (suggested order)

1. [ ] **Verify the update-order diagnosis with 30 seeds (ISSUE-016).**
   The starvation death rate of high-ID founders was 100% under fixed
   order and 33% under shuffled order, but this rests on 4 seeds. It determines
   the order in which subsequent experiments will be run.
   - **Decision needed:** should the default order be `shuffled`? The `fixed`
     option remains for repeating older experiments.
2. [ ] **Fix the foraging weakness in the need-based score.** The score
   multiplies the return on foraging by the belief about the stores; when the
   stores look empty, the agent does not forage even when deprived, and most
   starvation deaths occur in these arms. Candidate: let the agent learn the
   return from its own most recent foraging experience. This needs a separate
   protocol and a new seed block.
3. [ ] **Null model for Gini.** The same measurement with agents that only make
   random transfers; it determines what the Gini findings are to be read
   against ([REFERENCES.md](REFERENCES.md) #15).
4. [ ] **Identity bonus ablation.** The identity-experiment counterpart of what
   was done in the resource experiment (ISSUE-013); also a per-label wealth
   record to explain the Gini increase.
5. [ ] **Re-test the birth rate finding with 30 seeds** (ISSUE-007, ISSUE-012;
   currently 10 seeds).
6. [ ] **`provision_*` sensitivity.** Meaningful only in the deprivation regime;
   particularly `provision_max_per_tick`, which has no empirical basis.
7. [ ] **Paper outline.** Compiled from the ODD+D draft, the protocols, and the
   results reports. The main claim should not be written before 1 and 2 are
   finished.

## Later

- Comparison with the Epstein (2002) decision rule ("docking") — [REFERENCES.md](REFERENCES.md) #10–11.
- Mass conservation in foraging (loss of excess foraged resource).
- Splitting long experiments across several cores; results do not change
  because they depend on the seed, and the run time shortens.
- Verifying the dashboard in a real browser (ISSUE-010).

## Working rules

For every experiment, the protocol is written and committed before the run; a
new seed block is used; coefficients are not changed by looking at the results
([PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md)).
