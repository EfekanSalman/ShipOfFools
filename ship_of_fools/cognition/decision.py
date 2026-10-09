"""Decision-making: turns needs + personality + beliefs + stress into an action.

Deliberately a simple utility/softmax model, not deep RL — per
PROJECT_CONSTITUTION.md rule 5 ("use ML only where it adds explanatory value").
Kept easy to swap out later (V6: predictive processing / active inference).
"""
import math
import random

ACTIONS = ["forage", "rest", "socialize", "share", "steal", "spread_belief"]


def score_actions(agent, norms=None, identity_strength: float = 0.3, adulthood_age: int = 16,
                   self_correction_strength: float = 0.3, deterrence_strength: float = 0.5,
                   steal_scarcity_weight: float = 0.9, share_scarcity_weight: float = 0.5,
                   action_scarcity_reference: float | None = None,
                   need_based: bool = False, steal_relative_gain: float = 0.0) -> dict:
    n = agent.needs
    p = agent.personality
    if need_based:
        # ISSUE-014: the direct scarcity-belief terms are replaced by the
        # consequence terms added below.
        steal_scarcity_weight = share_scarcity_weight = 0.0
    # ISSUE-013: the share/steal scores read scarcity_belief directly. The
    # reference override cuts that link (the scores see a constant) without
    # touching the belief itself, so indirect channels stay intact.
    action_scarcity = (agent.beliefs.scarcity_belief if action_scarcity_reference is None
                       else action_scarcity_reference)
    scores = {
        "forage": (1 - n.food) * 1.2 + (1 - n.water) * 1.2 + p.conscientiousness * 0.3,
        "rest": (1 - agent.energy) * 1.3 + agent.stress * 0.4,
        "socialize": (1 - n.social) * 1.1 + 0.2 * p.dominance,
        "share": p.empathy * 0.9 - action_scarcity * share_scarcity_weight + (0.4 if agent.wealth > 15 else 0.0),
        "steal": (1 - p.conscientiousness) * 0.6 + action_scarcity * steal_scarcity_weight
                 + p.risk_tolerance * 0.4 - p.empathy * 0.5
                 - deterrence_strength * agent.beliefs.institution_trust,
        "spread_belief": p.dominance * 0.6 + agent.stress * 0.5 + (1 - p.conscientiousness) * 0.2
                 + agent.beliefs.scarcity_belief * 0.3,
    }
    if need_based:
        # Each term is the agent's need urgency times what the action does for
        # those needs in the engine. Foraging pays off less the emptier the
        # agent believes the stores are; a theft brings in provisions worth
        # steal_relative_gain of a forage, and sharing gives the same amount up.
        urgency = (1 - n.food) * 1.2 + (1 - n.water) * 1.2
        scores["forage"] -= urgency * agent.beliefs.scarcity_belief
        scores["steal"] += urgency * steal_relative_gain
        scores["share"] -= urgency * steal_relative_gain

    if norms is not None:
        # TASK-301: conformist agents lean toward whatever the ambient norm
        # currently is — this is what lets a norm become self-reinforcing (or,
        # if it has drifted toward "helping isn't normal here", self-eroding).
        pull = p.conformity * (norms.helping_norm - 0.5)  # signed: >0 pulls toward sharing
        scores["share"] += 0.4 * pull
        scores["steal"] -= 0.4 * pull

        # Second culture axis: authority_norm. A conformist agent in a
        # deferential culture (authority_norm high) is pulled AWAY from
        # theft (respecting whatever passes for law here) and TOWARD amplifying
        # the dominant narrative; in an autonomy-leaning culture the pull
        # reverses — less deference, less appetite for repeating the party line.
        authority_pull = p.conformity * (norms.authority_norm - 0.5)
        scores["steal"] -= 0.3 * authority_pull
        scores["spread_belief"] += 0.2 * authority_pull

    # TASK-302: an identity, once formed, keeps reinforcing the behavior that
    # built it — even independent of the agent's current needs/stress. This is
    # the "sunk cost" identity effect (doc 3, point 4): a "benefactor" keeps
    # sharing partly *because* that's who they are now, not only because
    # empathy/needs say so this particular tick.
    label = agent.identity.label
    if label == "leader":
        scores["spread_belief"] += identity_strength
        scores["socialize"] += 0.5 * identity_strength
    elif label == "benefactor":
        scores["share"] += identity_strength
    elif label == "opportunist":
        scores["steal"] += identity_strength
    elif label == "survivor":
        scores["forage"] += identity_strength

    # TASK-601: metacognitive self-correction — if an agent's own (possibly
    # biased) introspection says it's been more selfish than it's comfortable
    # with, conscientious agents actively correct toward sharing; agents low
    # on conscientiousness mostly ignore the signal (doc 2, point 2's
    # self-evaluation only sometimes changes behavior).
    gap = 0.5 - agent.metacognition.perceived_self_cooperation  # >0: "I've been too selfish lately"
    correction = agent.personality.conscientiousness * gap * self_correction_strength
    scores["share"] += correction
    scores["steal"] -= correction

    # TASK-401: children (below adulthood_age) don't meaningfully participate
    # in adult economic/political life yet — they play/socialize instead.
    # This is what makes a newborn a real (temporary) dependency cost rather
    # than an instant extra worker.
    if adulthood_age is not None and agent.age_years < adulthood_age:
        scores["forage"] *= 0.3
        scores["steal"] *= 0.2
        scores["share"] *= 0.2
        scores["spread_belief"] *= 0.2
        scores["socialize"] *= 1.3
    else:
        # TASK-402: a parent with a hungry/thirsty child among their local
        # ties gets a direct pull toward `share` — parental care, distinct
        # from generic empathy-driven sharing.
        needy_children = [c for c in agent.children if c.alive and min(c.needs.food, c.needs.water) < 0.3]
        if needy_children:
            scores["share"] += 0.5

    return {k: max(0.01, v) for k, v in scores.items()}


def choose_action(agent, rng: random.Random, norms=None, identity_strength: float = 0.3,
                   adulthood_age: int = 16, self_correction_strength: float = 0.3,
                   deterrence_strength: float = 0.5, steal_scarcity_weight: float = 0.9,
                   share_scarcity_weight: float = 0.5,
                   action_scarcity_reference: float | None = None,
                   need_based: bool = False, steal_relative_gain: float = 0.0) -> str:
    scores = score_actions(agent, norms=norms, identity_strength=identity_strength,
                            adulthood_age=adulthood_age, self_correction_strength=self_correction_strength,
                            deterrence_strength=deterrence_strength,
                            steal_scarcity_weight=steal_scarcity_weight,
                            share_scarcity_weight=share_scarcity_weight,
                            action_scarcity_reference=action_scarcity_reference,
                            need_based=need_based, steal_relative_gain=steal_relative_gain)
    # more conscientious agents are less random (lower "temperature")
    temp = 0.6 + 0.6 * (1 - agent.personality.conscientiousness)
    weights = {k: math.exp(v / temp) for k, v in scores.items()}
    total = sum(weights.values())
    r = rng.uniform(0, total)
    upto = 0.0
    for k, w in weights.items():
        upto += w
        if upto >= r:
            return k
    return "rest"
