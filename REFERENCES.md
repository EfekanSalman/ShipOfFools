# REFERENCES — inventory of scientific grounding

As required by PROJECT_CONSTITUTION rule 4 and doc 1 §14: for every mechanism,
"what it represents / why it exists / which research inspired it / how it was
approximated / what its limit is". This file is the **honest** version of that
inventory.

## The most important caveat first

**Most** of the mechanisms in this model were not derived from a body of
literature. I (Claude) wrote them as plausible-looking heuristic formulas, and
only afterwards **associated** some of them with a general phenomenon in the
literature. "Inspired by this paper" and "this paper's model was implemented"
are different things; the table below contains only the former, and in some
rows even that is weak. **None** of the numerical coefficients (0.3, 0.4, 0.6 …)
comes from empirical calibration.

## Verification status (how I checked the citations)

- **VERIFIED** = in this session, the citation details (author, year, journal,
  volume/pages) matched in web search results.
- **PARTIAL** = title/year/journal matched, but volume/pages were not
  confirmed in the search.
- **NOT VERIFIED** = written from my memory, not checked. Do not trust these;
  verify them yourself before using them.

| # | Source | Status |
|---|--------|-------|
| 1 | Watts, D. J. & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature* 393, 440–442. | VERIFIED |
| 2 | Nickerson, R. S. (1998). Confirmation bias: A ubiquitous phenomenon in many guises. *Review of General Psychology* 2(2), 175–220. | VERIFIED |
| 3 | Baumeister, R. F., Bratslavsky, E., Finkenauer, C. & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology* 5(4), 323–370. | VERIFIED |
| 4 | Mezulis, A. H., Abramson, L. Y., Hyde, J. S. & Hankin, B. L. (2004). Is there a universal positivity bias in attributions? A meta-analytic review of individual, developmental, and cultural differences in the self-serving attributional bias. *Psychological Bulletin* 130(5), 711–747. | VERIFIED |
| 5 | Esteban, J.-M. & Ray, D. (1994). On the measurement of polarization. *Econometrica* 62(4), 819–851. | VERIFIED |
| 6 | Freeman, L. C. (1978/79). Centrality in social networks: Conceptual clarification. *Social Networks* 1(3), 215–239. | NOT VERIFIED (from memory) |
| 7 | Gini, C. (1912) / standard definition of the Gini coefficient | NOT VERIFIED; standard, low risk |
| 8 | Morris, M. D. (1991). Factorial sampling plans for preliminary computational experiments. *Technometrics* 33(2), 161–174. (the "Morris-type" name of `sensitivity.py` refers to this) | NOT VERIFIED (from memory) |
| 9 | Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience* 11, 127–138. (only for the TASK-602b plan; not yet used in code) | NOT VERIFIED (from memory) |

## Mechanism → grounding table (honest classification)

Classes: **[E]** *associated* with an empirically well-documented phenomenon;
**[T]** theoretical/structural assumption; **[S]** purely heuristic/design
choice. None is "empirically calibrated" (**[K]**).

| Mechanism (file) | Class | Associated source / note |
|---|---|---|
| Social network topology: ring lattice + rewiring (`sociology/social_network.py`) | [T], clear source | #1. A **simplified** adaptation of the Watts–Strogatz generation algorithm; the k and rewire_prob values were chosen to suit the model, not calibrated to a real network. |
| Belief updating: prior-weighted blending (`cognition/beliefs.py`, `confirmation_bias`) | [E] weak association | #2. *Conceptually* related to the confirmation-bias literature; NOT a real Bayesian update, but a fixed-weight exponential average. The 0.6 coefficient is heuristic. |
| Negative events outweighing positive ones (`steal` → target −0.8 vs `share` → +0.6; `harshness` in `update_from_interaction`) | [E] weak association | #3. Consistent in direction with "Bad is stronger than good"; the magnitude ratios (−0.8/+0.6, 0.35/0.25) are not from the literature but heuristic. |
| Self-serving bias (`cognition/metacognition.py`) | [E] weak association | #4. The meta-analysis supports the existence of such a bias and its cultural/developmental differences; the formula in the model (`(1-openness) * stress multiplier`) was not derived from that meta-analysis, and the structure is heuristic. |
| Stress → perceptual bias (`+0.15 * agent.stress`, `engine.py`) | [S] | No source. |
| Personality traits (openness, conscientiousness, empathy…) (`agents/personality.py`) | [S] | Borrows the *names* from the Big Five literature but is NOT tied to BFI/NEO measurement, distributions or correlations; all are independent clipped Gaussian(0.5, 0.18). This is not a real personality model. |
| Need/stress/health dynamics (`engine._update_internal_state`) | [S] | No source. The constants (0.03, 0.08, 0.02…) were chosen so that the system behaves plausibly. |
| Utility/softmax decision making (`cognition/decision.py`) | [S] | The softmax choice rule is a standard computational technique; the score coefficients are a design choice. |
| Norm formation: exponential convergence to observed behaviour (`culture/norms.py`) | [T] | Conceptually related to the social norm / conformity literature; not based on a specific model. |
| Identity formation and consolidation (`agents/identity.py`) | [S] | Loosely related to identity theory; the 5-repetition threshold and the 1.3× stickiness constant are inventions. |
| Leadership emergence: trust-weighted influence score (`institutions/leadership.py`) | [S] | No source. |
| Capture/deterrence, education, health, media institutions | [S] | No source; only the structural assumption that "institutions scale with legitimacy". |
| Ageing/reproduction/death (`population/lifecycle.py`) | [S] | NOT tied to a real life table / fertility data. `elderly_age=60`, `ticks_per_year=15`, etc. are arbitrary. |
| Resource pool and regeneration (`economy/resources.py`) | [S] | No source; a simple stock-flow abstraction. |
| Need-based decision architecture and edible provisions (`decision_architecture="need_based"`; `cognition/decision.py`, `engine._update_internal_state`) | [T] | #19–20: the attractiveness of an action is computed from its yield for the need. Only the structure was borrowed; the `provision_*` values and the score form are this codebase's choices, not calibrated. Not the default. |
| Polarization metric (`metrics/social_metrics.py`) | [E] source clear for the metric definition | #5. The measurement definition is from the source; **the choice of alpha=1.6 and 10 bins** was taken as this codebase's choice — the paper discusses α within the range [1, 1.6]; this does not mean "α=1.6 is the correct value", it is an upper bound. The number of bins affects results; sensitivity was not tested. |
| Network centralization (`social_metrics.py`) | [T] source for the definition | #6, not verified. The implementation is in-degree centralization normalised to the star-graph maximum; `test_social_metrics_known_cases` verified it on known graphs (star→>0.9, ring→~0). |
| Clustering coefficient (`social_metrics.py`) | [T] | #1. Estimated by sampling (for >300 nodes). |
| Social mobility: wealth rank correlation between two time points | [S] | A common rank-persistence idea; not tied to a specific source. **NOT intergenerational mobility** (newborns have no earlier rank). |
| "Foolishness" index (`Agent.foolishness`) | [S] | Entirely specific to this project, an arbitrarily weighted composite; does not correspond to any psychometric measure. |

## What is not measured, and why

- **Innovation / knowledge accumulation:** The model has no mechanism for
  producing technology or ideas; any "innovation" number would be fabricated.
  Instead only `human_capital_total` (the sum of `forage_skill`) is reported,
  and this is an approximation of skill accumulation, not innovation.
- **GDP-like output:** There are no prices/markets, so a meaningful aggregate
  output cannot be defined. Nothing was added beyond `human_capital_total` and
  total wealth.

## Related literature and design sources (review of 2026-10-07)

This section lists sources **not yet applied** to the model: candidates that
could be used in resolving ISSUE-013/014 and in positioning the findings. The
citation details were matched in this session by web search (author, year,
venue); the full text of the papers was not read, and the "what it means"
column is my (Claude's) interpretation.

| # | Source | Status | What it means for this project |
|---|--------|--------|----------------------|
| 10 | Epstein, J. M. (2002). Modeling civil violence: An agent-based computational approach. *PNAS* 99 (Suppl. 3). | VERIFIED | Decision rule: grievance = hardship × (1 − legitimacy); risk = risk aversion × arrest probability. The `steal` score uses the same components (scarcity, `institution_trust`, `risk_tolerance`, capture) with additive, heuristic coefficients. A candidate alternative decision rule and "docking" target. |
| 11 | Axtell, R., Axelrod, R., Epstein, J. M. & Cohen, M. D. (1996). Aligning simulation models: A case study and results. *Computational and Mathematical Organization Theory* 1, 123–141. | VERIFIED | "Docking": a method for testing whether two models produce the same result. A validation step that can be carried out in the absence of empirical data. |
| 12 | Brander, J. A. & Taylor, M. S. (1998). The simple economics of Easter Island: A Ricardo-Malthus model of renewable resource use. *American Economic Review* 88(1). | VERIFIED (volume/issue from memory) | Renewable resource + population = a Lotka-Volterra-type "boom and bust" cycle. A comparison model for the overshoot-collapse pattern in ISSUE-006/007. |
| 13 | Prediger, S., Vollan, B. & Herrmann, B. (2014). Resource scarcity and antisocial behavior. *Journal of Public Economics* 119, 1–9. | VERIFIED | Field experiment: antisocial behaviour is twice as high in the scarce region. An empirical source supporting the sign (not the magnitude) of `steal_scarcity_weight`. |
| 14 | von Dawans, B., Fischbacher, U., Kirschbaum, C., Fehr, E. & Heinrichs, M. (2012). The social dimension of stress reactivity: Acute stress increases prosocial behavior in humans. *Psychological Science* 23(6), 651–660. | VERIFIED | Acute stress **increases** trust and sharing. The sign in the model, "scarcity/stress → less sharing", is not the only possible direction; the sign should be an experimental factor. |
| 15 | Drăgulescu, A. & Yakovenko, V. M. (2000). Statistical mechanics of money. *European Physical Journal B* 17, 723. | VERIFIED | Random pairwise transfer of a conserved quantity alone produces an exponential distribution (Gini 0.5). A null model for the `steal`/`share` transfers; Gini findings should be read against it. |
| 16 | Bem, D. J. (1972). Self-perception theory. *Advances in Experimental Social Psychology* 6, 1–62. | VERIFIED | A person infers their attitudes from their own behaviour. The closest theoretical grounding for the `agents/identity.py` and `metacognition.py` mechanisms ([S] → weak [E]). |
| 17 | Edmonds, B. & Moss, S. (2005). From KISS to KIDS — an 'anti-simplistic' modelling approach. *Multi-Agent and Multi-Agent-Based Simulation*, Springer. | VERIFIED | The position that defends multi-mechanism models: build descriptively first, simplify when evidence requires it. Ablation is the instrument of this simplification. |
| 18 | Starr, P. (1994). Seductions of Sim: Policy as a simulation game. *The American Prospect* 17, 19–29. | VERIFIED | The SimCity critique: assumptions sit in an inaccessible black box; the player mistakes the model's rule for the law of the world. ISSUE-013 as it stood in 1994. |
| 19 | Forbus, K. D. & Wright, W. (2001?). Some notes on programming objects in The Sims. Northwestern University lecture note. | VERIFIED (year from memory) | Objects "advertise" need satisfaction; the Sim weights the advertisement by its current need. A design pattern for ISSUE-014. |
| 20 | Zubek, R. (2010). Needs-based AI. *Game Programming Gems 8*. | PARTIAL (book and author matched; chapter content from memory) | An explicit account of the same architecture; nonlinear decay curves by need level. |
| 21 | Willmott, A. (2012). Inside GlassBox. GDC 2012 talk. | VERIFIED | The SimCity (2013) engine: Resources, Units, Maps, Globals; city-level behaviour emerges from agents. |
| 22 | Gingold, C. (2024). *Building SimCity: How to Put the World in a Machine.* MIT Press. | VERIFIED | The Forrester system dynamics and cellular automata origins of SimCity; Maxis history. |
| 23 | Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST '23*. | VERIFIED | Language-model-based agents in an environment inspired by The Sims. Not recommended for the core under Constitution rule 5; comparison literature. |

Not checked in this session, from memory (verify before use): Epstein &
Axtell (1996) *Growing Artificial Societies* (Sugarscape); Forrester (1969)
*Urban Dynamics*; Meadows et al. (1972) *The Limits to Growth*; Watson &
Lovelock (1983) Daisyworld; McKelvey & Palfrey (1995) quantal response
equilibrium (the game-theoretic counterpart of the softmax choice rule);
Ostrom (1990) *Governing the Commons*.

## Limit of this file

This is NOT a literature review. The searches answer only the question "is
this citation real"; they do not answer "how well does this mechanism overlap
with that source" — that judgement is still mine and weak. A real grounding
study would require, for each [S] row, finding a value calibrated from the
field's literature, or explicitly leaving that row as a "design choice".
