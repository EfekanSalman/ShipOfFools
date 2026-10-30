# Ship of Fools — an academic agent-based simulation

Ship of Fools is an agent-based simulation research project developed to study
individual psychology, social relations, institutions, culture, and resource
dynamics in a ship environment. The model aims to generate behaviour from the
interaction of personality, needs, stress, beliefs, and social ties.

This code base is a research tool; it does not claim to reproduce the behaviour
of real people or neurobiology in a validated way. A significant share of the
mechanisms and coefficients are design assumptions. For the status of sources
and the model's limitations, see [REFERENCES.md](REFERENCES.md),
[KNOWN_ISSUES.md](KNOWN_ISSUES.md), and [REVALIDATION.md](REVALIDATION.md).

## Installation

Python 3.10 or later is required. `requirements.txt` installs `matplotlib` for
PNG plots and `scipy` for the statistical re-testing module. Windows
PowerShell:

```powershell
cd ship_of_fools_project
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

macOS/Linux:

```bash
cd ship_of_fools_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Run the commands from the project folder:

```bash
python run.py                         # single run; produces output/metrics.csv and a PNG
python run_experiments.py             # baseline vs. misinformation comparison
python run_v5_lab.py                  # long multi-seed experiment; may take a few minutes
python run_sensitivity.py             # Morris-type parameter screening
python run_interaction_test.py        # two-parameter 2x2 factorial experiment
python run_revalidation.py            # statistical re-testing; roughly a few minutes
python run_scale_test.py              # short runtime scaling measurement
python run_dashboard.py --agents 80 --ticks 500 --seed 42
python run_regime_calibration.py      # resource scarcity pilot sweep; may take a few minutes
python run_resource_factorial.py     # final 2x2 experiment; 120 worlds, a few minutes
python run_schedule_robustness.py    # fixed vs. per-tick shuffled order comparison
python analyze_schedule_robustness.py # factorial contrast analysis for the scheduling results
python run_agent_rng_robustness.py   # 240 schedule runs with per-agent RNG and matched seeds
python analyze_agent_rng_robustness.py # produces the per-agent RNG robustness analysis
python run_identity_resource_factorial.py # resource regime × identity feedback; 240 worlds
python analyze_identity_resource_factorial.py # seed-blocked paired bootstrap analysis
python run_scarcity_link_ablation.py  # resource × scarcity-belief link ablation; 360 worlds
python analyze_scarcity_link_ablation.py # ablation contrasts and retained fraction
python run_identity_label_followup.py # label/action shares of the identity experiment; 240 worlds
python run_scarcity_link_ablation.py --arms intact,need_based --seed-start 70000 --out-dir output/need_based_decision --protocol EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md  # need-based decision architecture; 240 worlds
python analyze_scarcity_link_ablation.py --dir output/need_based_decision
python run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based --seed-start 80000 --out-dir output/provision_scoring_factorial --protocol EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md  # provisions × scoring decomposition; 480 worlds
python analyze_scarcity_link_ablation.py --dir output/provision_scoring_factorial --factorial provisions_only,scoring_only,need_based
python run_deprivation_pilot.py       # deprivation regime calibration; also run with --order shuffled
python run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based --capacities 90,120 --regen-rates 0.004,0.010 --order shuffled --seed-start 94000 --out-dir output/deprivation --protocol EXPERIMENT_PROTOCOL_DEPRIVATION.md  # true deprivation; 480 worlds
python analyze_scarcity_link_ablation.py --dir output/deprivation --factorial provisions_only,scoring_only,need_based
python ship_of_fools/tests/test_basic.py
python ship_of_fools/tests/test_reproducibility.py
python ship_of_fools/tests/test_resource_factorial.py
python ship_of_fools/tests/test_schedule_robustness.py
python ship_of_fools/tests/test_scarcity_link_ablation.py
python ship_of_fools/tests/test_need_based_decision.py
```

The dashboard produces an HTML file; because it loads its charting libraries
from a CDN, an internet connection is required to view it. The simulation
engine and the regime calibration pilot use the Python standard library; PNG
plots require `matplotlib`, and `run_revalidation.py` requires `scipy`.

Record the seed and parameters in every experiment. Report results over
multiple runs, using matched seeds where possible; do not interpret a single
run as evidence. Experiment outputs are written under `output/`. The tick-level
`timeseries` CSV files (9–65 MB) are not kept in git; the corresponding
`run_*.py` script regenerates them with the same seeds. Seed summaries,
experiment metadata, and analysis files are in the repository.

## Model scope

The current model includes:

- Continuous personality traits, needs, stress, energy, mood, and health.
- Noisy perception of the environment, belief updating, rumour spread, and
  simple metacognitive self-assessment.
- A small-world neighbourhood network, trust relations, mental models, and
  partial second-order theory of mind.
- A shared resource pool, forage/share/steal actions, and wealth measures.
- Organic leadership, taxation and redistribution, policing, education, health,
  and partial media mechanics.
- Norm formation, two norm axes, behaviour-derived identities, and simple
  intergenerational transmission; birth, ageing, and death.
- Time-series metrics, social network measures, multi-seed experiments,
  counterfactual comparisons, and sensitivity and interaction analyses.

The detailed module structure and tick flow are in
[ARCHITECTURE.md](ARCHITECTURE.md), the code-based ODD+D draft in
[ODD_D.md](ODD_D.md), the academic method and experiment plan in
[ACADEMIC_RESEARCH_PLAN.md](ACADEMIC_RESEARCH_PLAN.md), the resource experiment
protocol in
[EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md](EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md),
the experiment results report in
[RESOURCE_STRESS_RESULTS.md](RESOURCE_STRESS_RESULTS.md), the update-order
robustness report in
[SCHEDULE_ROBUSTNESS_RESULTS.md](SCHEDULE_ROBUSTNESS_RESULTS.md), the per-agent
RNG robustness report in
[AGENT_RNG_ROBUSTNESS_RESULTS.md](AGENT_RNG_ROBUSTNESS_RESULTS.md), the
identity × resource factorial protocol in
[EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md](EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md)
and its results in [IDENTITY_RESOURCE_RESULTS.md](IDENTITY_RESOURCE_RESULTS.md),
the scarcity-belief link ablation protocol in
[EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md](EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md)
and its results in
[SCARCITY_LINK_ABLATION_RESULTS.md](SCARCITY_LINK_ABLATION_RESULTS.md), the
need-based decision architecture protocol in
[EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md](EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md)
and its results in [NEED_BASED_DECISION_RESULTS.md](NEED_BASED_DECISION_RESULTS.md),
the provisions × scoring decomposition protocol in
[EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md](EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md)
and its results in
[PROVISION_SCORING_FACTORIAL_RESULTS.md](PROVISION_SCORING_FACTORIAL_RESULTS.md),
and the true deprivation protocol in
[EXPERIMENT_PROTOCOL_DEPRIVATION.md](EXPERIMENT_PROTOCOL_DEPRIVATION.md) and its
results in [DEPRIVATION_RESULTS.md](DEPRIVATION_RESULTS.md).
The staged development plan is in [TASK_GRAPH.md](TASK_GRAPH.md).

## Scientific interpretation and known limitations

- Most model coefficients have not been calibrated empirically. Being inspired
  by the scientific literature does not, by itself, mean that a mechanism has
  been validated.
- In the default parameter regime, scarcity approaches a ceiling effect; some
  results may change in other regimes. The sensitivity sweep does not fully
  cover parameter interactions.
- Some older findings rest on small samples or lack confidence intervals; their
  re-testing status is noted in `REVALIDATION.md` and `KNOWN_ISSUES.md`.
- The dashboard is a first slice: it shows a limited number of agents and the
  last-tick network; end-to-end visual verification in a real browser has not
  yet been completed.
- The economy has no price/labour market. Culture is limited to two simple
  norms; full nested theory of mind and predictive processing do not exist yet.

These limits keep the evaluation of scientific results within the scope of the
model; open items are tracked in [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Project structure

```text
ship_of_fools/
  agents/ cognition/ sociology/ information/ economy/ environment/
  institutions/ culture/ population/ simulation/ metrics/ experiments/
  visualization/ tests/
run*.py                 simulation and experiment entry points
ARCHITECTURE.md         actual module structure and tick flow
PROJECT_CONSTITUTION.md modelling and development principles
TASK_GRAPH.md           roadmap and remaining tasks
KNOWN_ISSUES.md         open issues and decision history
REFERENCES.md           mechanism–source mapping and evidence notes
REVALIDATION.md         statistical re-testing results
requirements.txt        runtime dependencies
```
