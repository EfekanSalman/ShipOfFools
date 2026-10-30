# Academic Research and Simulation Plan

This document collects the methods, priorities and the proposed first study
to be used in developing Ship of Fools as an agent-based simulation for
research purposes. This plan does not mean that the model already validates
real human behaviour. The current model is primarily a research tool for
examining theoretical mechanisms and their consequences in an artificial world.

## 1. Academic framework

### Level of claim made by the model

The following distinction will be maintained at every stage of the work:

- **Code verification (verification):** Does the code implement the intended rules?
- **Conceptual validation:** Are the chosen mechanisms consistent with the
  research question and the theories they rest on?
- **Behavioural evaluation:** Do the patterns the model produces match
  expected or observed patterns?
- **Empirical calibration/validation:** Were the parameters chosen according to
  real data; were the results tested against unused data or an independent pattern?

Success at one stage is not counted as evidence for the other stages. Unless the
model is tied to real data, results will not be presented as “this is what
happens in a real society”; they will be reported as “observed in the model
under these assumptions”.

### Model documentation: ODD and ODD+D

The current code should be documented in the ODD (Overview, Design concepts,
Details) structure, with enough clarity for others to rebuild it. ODD covers
purpose, agents/state variables and scales, process order, design concepts,
initialisation, inputs and submodels. Because we include human decisions, the
ODD+D questions on decision makers, options, the decision process, learning and
information assumptions should also be applied.

Concrete topics to be documented:

- What information does an agent actually see, and what does it carry only as
  an erroneous belief?
- What are the options, scores/probabilities and parameters of each decision?
- Which process runs in which order, over which set of agents?
- If agents learn or adapt, exactly which variable is updated?
- How are the initial population, its ages, resource levels and the network
  constructed?
- Which theory does each mechanism rest on; which parts of it are design
  assumptions?

### Pattern-oriented evaluation

Instead of declaring the model “valid” with a single overall score, a few
observable patterns relevant to the research question should be selected in
advance. Where possible, patterns at different levels should be considered
together (agent behaviour, network/institution, population or time series). It
should also be compared whether alternative mechanisms produce the same
pattern. Where there is no target pattern and no data, the result should be
classified as theoretical/exploratory; no claim of empirical validation should
be made.

## 2. Initial observation from the current run

In a single run with the default configuration (80 agents, 500 ticks, seed 42):

- `true_scarcity` reached 1.0 at tick 300 and stayed at the ceiling until the
  end of the run.
- Stress rose; trust fell from a slightly positive initial value to negative.
- Cooperation fell relative to the start; conflict and Gini rose.
- Population rose to 102 and fell back to 76.

This is only **a descriptive observation for one configuration and seed**; it
is not a generalised finding. The default scarcity ceiling is a regime/sensitivity
problem that needs to be addressed before further research (see also
`KNOWN_ISSUES.md` ISSUE-011/012).

### First scarcity-regime pilot (2026-10-04)

With `run_regime_calibration.py`, 80 agents, 400 ticks, analysis of the last 100
ticks and 16 parameter combinations (capacity 75/90/105/120 × regen
0.010/0.013/0.016/0.019) were run. Each cell received 4 separate seeds; the
seed ranges are disjoint across candidates (10000–10063). The criterion defined
in advance: mean scarcity 0.30–0.60 and scarcity ≥0.98 in at most 10% of the
ticks in the analysis window.

| Capacity/agent | Food+water regen | Last-window scarcity mean ± between-seed SD | Share of ticks at ceiling | Criterion |
|---:|---:|---:|---:|---|
| 90 | 0.019 | 0.515 ± 0.088 | 0.0% | meets |
| 120 | 0.016 | 0.337 ± 0.151 | 0.0% | meets |
| 105 | 0.016 | 0.579 ± 0.228 | 0.0% | meets |

By the scarcity criterion, the first candidate was **capacity 90, regen 0.019**.
Cooperation and conflict rates were reported exploratorily in the output file;
they did not affect the ranking. Four seeds are sufficient only for a
preliminary screen; this candidate is not a final calibrated setting. Full
result: `output/regime_calibration_pilot.json`.

**Next step:** this first candidate and at least one suitable alternative were
re-examined in wider, mutually independent new pilot seed blocks. On 2026-10-04
a 2×2 follow-up screen was run (80 agents, 500 ticks, last 100 ticks, 20 seeds
in each cell; seed blocks 20000–20079):

| Capacity/agent | Regen | Scarcity mean ± between-seed SD | Seed mean in target band | Share of ticks at ceiling | Criterion |
|---:|---:|---:|---:|---:|---|
| 120 | 0.016 | 0.582 ± 0.189 | 11/20 (55%) | 4.1% | passed mean/ceiling criterion |
| 120 | 0.019 | 0.232 ± 0.179 | 8/20 (40%) | 0.0% | mean below target |
| 90 | 0.019 | 0.853 ± 0.136 | 1/20 (5%) | 35.9% | scarcity high/too much at ceiling |
| 90 | 0.016 | 0.989 ± 0.032 | 0/20 (0%) | 89.2% | scarcity stuck at ceiling |

Important result: the `90 / 0.019` setting that stood out in the first pilot
did **not replicate** moderate scarcity in the new seed block. Although the
`120 / 0.016` setting is within the target band on the 20-seed mean and has a
low ceiling share, the last-window mean entered the target band in only 11/20
of the seeds; between-seed variability is high. Therefore we have not yet found
a reliable/stable moderate regime. This shows that candidate selection should
not be based on a single mean and that run-to-run variability should be treated
as part of the research result.

Full result: `output/regime_calibration_confirmation.json`. The coop/conflict
columns are exploratory and did not take part in the regime ranking. Decision:
we are not forcing a search for a single stable moderate-scarcity setting
through wider calibration. Instead, we will fix the capacity×regeneration
factorial conditions and test the effect of resource regimes on the outcome
distribution. The detailed protocol is in `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md`.

## 3. Working principles

1. **Question first, then feature:** Before adding a new subsystem, write down
   which research question and measurable hypothesis it serves.
2. **Separate claim from evidence:** An in-simulation pattern, agreement with
   empirical data, and causality are separate claims.
3. **Justify mechanisms:** Record the source, theory, simplification and limit
   for each mechanism; when no source can be found, mark this explicitly as a
   “design assumption”.
4. **Evaluate model layers separately:** Code correctness, mechanism behaviour,
   whole-model patterns and empirical comparison are separate stages.
5. **Use multiple patterns and runs:** Report the seed distribution. Do not
   choose the number of seeds as a fixed magic threshold; justify it until the
   uncertainty interval or a precision target defined in advance is sufficient.
6. **Separate calibration and evaluation runs:** Do not reuse in the final
   hypothesis test the seeds used when selecting parameters/regimes.
7. **Test alternative structures:** Examine whether the result depends not only
   on changing coefficients but also on plausible alternative decision
   rules/network structures.
8. **Store reproduction information:** Code version, parameters, seeds,
   Python/dependency versions, experiment definition, raw results and analysis
   summary should be stored together.
9. **Do not tune coefficients according to the direction of the result:** Do not
   force mechanism coefficients after the fact to support a desired hypothesis;
   tuning must be justified by the research question and tested on separate data.

## 4. Critical technical issue: seed matching

The simulation uses a single `Simulation.rng` stream across many processes.
Even if two conditions start with the same seed, the number and order of random
draws can diverge once the conditions produce different behaviours. Therefore,
even though `run_paired_counterfactual` uses the same seed, it should not be
assumed that seed matching guarantees common random shocks over the ticks.

Before using a paired design, one of the following options should be evaluated
and documented:

- Using independent seeds in each condition and comparing the condition
  difference through the seed distributions.
- If common random numbers are required, designing independent RNG streams per
  process/agent/tick or keyed deterministic random draws; testing their
  compatibility with the existing reproducibility records.

Whichever design is chosen, the RNG layout and version should be written to the
experiment output.

## 5. Proposed research questions

### A. Resource pressure, cooperation and conflict — proposed first study

**Research question:** How does resource scarcity change cooperation and
conflict patterns under the model's defined conditions? Is this relationship
linear; does it depend on the initial trust/network structure or on
institutional conditions?

**Why first:** The resource pool, stress, action selection and population
dynamics are coupled in the current engine. Because the pilots showed regime
differences across seeds, the research will not merely look for a fixed
“moderate scarcity” level; it will measure the outcome distributions and
interaction of capacity/regeneration conditions.

**To be measured in the first stage:** `true_scarcity`, stress,
cooperation/conflict rate, trust, inequality, population and deaths. Rather than
settling for the final-tick value, a pre-defined last-period window and the
full time series should be reported.

**Important design rule:** Resource parameters are set as research conditions;
once the condition results are seen, they are not re-tuned to obtain target
cooperation/conflict values. Pilot seeds do not take part in the final analysis.

### B. Real and perceived institutional legitimacy

How does the difference between an institution's real legitimacy and agents'
beliefs affect behaviours and the institution's persistence? First, the
measurement and mechanism chain of the institutional variables should be
clarified; the rarity of leadership formation should be taken into account in
the design.

### C. Identity consolidation, network structure and trust

What is the link between behaviour-derived identities and trust relationships
and network clustering? The current identity feedback and network metrics can
provide a starting point; alternative identity-formation rules and adequate
sample sizes are needed.

### D. Institutions, scarcity and distribution

In which resource regimes do taxation/redistribution or law enforcement change
outcomes? Before testing this, it is necessary to define explicitly the
formation of leadership/legitimacy and which agents the intervention is applied
to and when.

## 6. Proposed staged roadmap

**Status of progress:** The first code-based draft of ODD+D has been added; the
same-seed reproducibility check passed; the first 16-cell screen and the
20-seed 2×2 follow-up screen were run. Because no replicable “moderate regime”
was found, a 2×2 final experiment protocol treating the seed distribution as
the result was implemented and the final run was completed. Results are in
`RESOURCE_STRESS_RESULTS.md`.

### Stage 1 — Research scope and model description

- The first question (resource pressure → cooperation/conflict) and the
  theoretical/exploratory starting framework were chosen.
- `ODD_D.md` was created: let us document the current code and the human
  decision mechanisms under the ODD+D headings, based on the actual implementation.
- Let us link the existing `REFERENCES.md` sources and the points that are
  “design choices” to ODD+D, mechanism by mechanism.

### Stage 2 — Code verification and reproduction

- It was tested that the full metric trajectory is identical for the same
  configuration/seed.
- The factorial analysis function, known 2×2 contrasts and a small CLI run were
  smoke-tested.
- The full `test_basic.py` run could not be completed in the first environment
  because SciPy was not present. On 2026-10-07 the entire test suite passed in
  an environment with SciPy installed (Python 3.14).
- Determine tests covering boundary values, population/resource/probability
  invariants and the important process order.
- Decide on the seed-matching design; fix the experiment output schema.

### Stage 3 — Scarcity-regime calibration

- The first screen and the 2×2 follow-up with 20 seeds/cell were done; it was
  seen that the moderate-scarcity candidates were not stable across seeds.
- Decision: we are not forcing the selection of a single “moderate”
  configuration; we are fixing the capacity levels 90/120 and regeneration
  levels 0.016/0.019 as the final experiment conditions.
- Pilot and final seeds were separated; parameters, seeds, summaries and time
  series are written to machine-readable files.

### Stage 4 — Pre-defined experiment

- The `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md` protocol was written; the 2×2
  conditions, hypotheses, unit (seed), metric window and bootstrap contrasts
  were defined.
- The final experiment was completed: 30 seeds/cell; bootstrap 95% CI. 30 seeds
  is not a universal guarantee of adequacy; the seed-level uncertainty is shown
  in the results report.
- Result tables, seed distributions and interpretation limits are in
  `RESOURCE_STRESS_RESULTS.md`; raw JSON and CSV files are in
  `output/resource_factorial/`.

### Stage 5 — Structural robustness and sharing

- Plan to test the main result with plausible alternative parameter regimes and
  mechanism choices.
- Complete the installation, command-line interface, data dictionary and ODD+D
  document in a reproducible way.
- Later, if deemed appropriate, prepare for publication according to the
  documentation and sharing standards of computational model archives such as
  CoMSES Net.

## 7. Decision log and next questions

Initial decisions were made and the first coding slice was completed:

- First research focus: **resource capacity/regeneration → cooperation and conflict**.
- First level of claim: **theoretical/exploratory within-model analysis**.
- Decision: because moderate scarcity is unstable across seeds, the final
  experiment will look at the outcome distributions in the 2×2 resource
  conditions rather than at a single moderate regime.
- First implementation: the ODD+D document, the seed reproducibility check, the
  regime pilot calibrator, the protocol and the factorial experiment runner were
  prepared.

The update-order robustness analysis was completed: the same 120 seed-condition
pairs were run with shuffled agent order. The bootstrap intervals of the nine
primary factorial effect differences covered zero, and the directions of the
capacity/regeneration effects remained the same. This is not equivalence
evidence; seed matching is not a full common-random-numbers design. Then, in a
240-run follow-up, the action RNG streams were separated per agent and the same
comparison was repeated; the primary contrasts again preserved their direction.
Details are in `SCHEDULE_ROBUSTNESS_RESULTS.md` and
`AGENT_RNG_ROBUSTNESS_RESULTS.md`. `shared` remains the current default; which
mode to prefer for research is a separate methodological decision.
In a subsequent follow-up, the old `identity_feedback_strength` finding was
crossed with the 2×2 resource conditions (0.0/0.5; 30 paired seed blocks/cell).
The trust and conflict effects came out in the same direction in all regimes;
the increase in conflict and the decrease in cooperation were larger at low
capacity. The method is in `EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md`, the
results in `IDENTITY_RESOURCE_RESULTS.md`. This analysis is also within-model;
intermediate doses and mechanism decomposition are open work.
The full test suite was re-run on 2026-10-07 in an environment with SciPy
installed and passed.

2026-10-07 review: the primary results of the resource and identity experiments
depend on direct terms in the decision formula (`scarcity_belief` in the
`steal`/`share` scores; the `steal` bonus on the `opportunist` label) —
ISSUE-013. Within the scope of Principle 7 and Stage 5, a 2×2×3 ablation
experiment that severs the direct link was run according to a protocol
(`EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`); the results are in
`SCARCITY_LINK_ABLATION_RESULTS.md`. The label/action distribution of the
identity experiment was extracted post hoc (appendix to `IDENTITY_RESOURCE_RESULTS.md`).

2026-10-09: the alternative, need-based decision architecture (ISSUE-014) was
tested with a 2×2×2 protocol (`NEED_BASED_DECISION_RESULTS.md`). The scarcity →
conflict relationship came out in the same direction but about one eighth in
magnitude. Taken together, the three experiments show that the magnitude of
this relationship depends on the decision-rule assumption; the main result to
be reported is this structural uncertainty.

2026-10-09 (continued): the provisions × scoring decomposition showed that the
difference belongs to the scoring form (`PROVISION_SCORING_FACTORIAL_RESULTS.md`).
It was found that `true_scarcity` measures store fullness, that agents are well
fed even at the ceiling (ISSUE-015), and that fixed agent order produces
priority by agent ID under scarcity (ISSUE-016). In the real-deprivation
experiment set up with shuffled order (`DEPRIVATION_RESULTS.md`), the direction
of the effect of deprivation on the conflict measure turned out opposite
depending on the decision rule. The main result widened: the scarcity →
conflict relationship depends both on whether scarcity is a belief or a
deprivation and on the decision rule.

## References

- Grimm et al. (2020), “The ODD Protocol for Describing Agent-Based and Other
  Simulation Models”: <https://doi.org/10.18564/jasss.4259>
- Müller et al. (2013), “Describing human decisions in agent-based models —
  ODD+D”: <https://doi.org/10.1016/j.envsoft.2013.06.003>
- Grimm et al. (2005), “Pattern-Oriented Modeling of Agent-Based Complex
  Systems”: <https://doi.org/10.1126/science.1116681>
- Windrum, Fagiolo & Moneta (2007), “Empirical Validation of Agent-Based
  Models: Alternatives and Prospects”: <https://jasss.soc.surrey.ac.uk/10/2/8.html>
- CoMSES Net, model and documentation standards:
  <https://www.comses.net/resources/standards/>
