"""Plot simulation metrics over time."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_timeseries(rows, out_path: str, title: str = "Ship of Fools — V0"):
    ticks = [r["tick"] for r in rows]
    fields = ["population", "avg_age", "avg_stress", "avg_trust", "positive_relationship_rate", "negative_relationship_rate",
              "avg_scarcity_belief", "true_scarcity",
              "avg_foolishness", "cooperation_rate", "conflict_rate", "inequality_gini",
              "avg_reflected_self", "social_perception_gap",
              "has_leader", "institution_legitimacy", "avg_institution_trust", "helping_norm",
              "authority_norm", "avg_health",
              "identity_formed_rate", "avg_perceived_self_cooperation", "avg_forage_skill",
              "belief_polarization", "wealth_polarization", "trust_centralization"]
    fig, axes = plt.subplots(len(fields), 1, figsize=(9, 1.7 * len(fields)), sharex=True)
    for ax, field in zip(axes, fields):
        ys = [r.get(field) for r in rows]
        ax.plot(ticks, ys, linewidth=1.2)
        ax.set_ylabel(field, fontsize=8)
        ax.grid(alpha=0.3)
    axes[-1].set_xlabel("tick")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
