import time
import random
import statistics
import math
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional

import networkx as nx
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

# --- SIMULATION CONFIGURATION ---
POPULATION_SIZE = 15
INITIAL_RESOURCES = 200
GAME_SPEED = 1.0


# --- 1. PSYCHOLOGICAL DEPTH LAYERS ---

@dataclass
class BigFive:
    openness: float  # 0.0 to 1.0 (High = Radical ideas, Low = Traditionalist)
    conscientiousness: float  # High = Dutiful/Loyal, Low = Opportunistic
    extraversion: float  # High = Leader/Loud, Low = Silent Majority
    agreeableness: float  # High = Cooperative, Low = Conflict/Predatory
    neuroticism: float  # High = Prone to PTSD/Panic, Low = Stoic


class Agent:
    def __init__(self, uid: int, name: str, role: str):
        self.uid = uid
        self.name = name
        self.role = role

        # 1. Personality Generation
        self.psyche = BigFive(
            openness=random.random(),
            conscientiousness=random.random(),
            extraversion=random.random(),
            agreeableness=random.random(),
            neuroticism=random.random()
        )

        # 2. State Vectors
        self.hunger = 0.0  # 0 to 100
        self.radicalization = 0.0  # 0 to 100 (Ideological Extremism)
        self.trauma = 0.0  # Accumulates. High trauma = Behavioral shift
        self.resources = random.randint(1, 5)  # Private stash (Food/Money)

        # 3. Social Logic
        self.influence_score = 0.0  # Calculated via PageRank/Centrality
        self.secret_allegiance = None  # "Shadow Cabinet" or "Loyalist"
        self.is_scapegoat = False

    def react_to_event(self, event_severity: float, global_moral_decay: float):
        """
        Psychological reaction function.
        Neurotic agents gain Trauma faster.
        Trauma leads to Radicalization.
        """
        stress = event_severity * self.psyche.neuroticism
        self.trauma += stress

        # PTSD Mechanism: If trauma triggers, personality shifts
        if self.trauma > 50 and random.random() < 0.1:
            self.psyche.agreeableness = max(0.0, self.psyche.agreeableness - 0.2)
            self.psyche.neuroticism = min(1.0, self.psyche.neuroticism + 0.1)
            return f"{self.name} has developed PTSD. They are becoming aggressive."

        # Radicalization Logic (Echo Chamber effect)
        # If society is decaying (high global_moral_decay), low conscientiousness agents turn to crime/rebellion
        if global_moral_decay > 50 and self.psyche.conscientiousness < 0.4:
            self.radicalization += 5
            return f"{self.name} is radicalizing due to moral decay."

        return None

    def decide_action(self, global_food: int, taboo_threshold: float) -> str:
        """
        Decision Tree based on Maslow's Hierarchy & Moral Decay (Overton Window).
        """
        # SURVIVAL (Hunger Games Mechanic)
        if self.hunger > 80:
            if self.resources > 0:
                self.resources -= 1
                self.hunger -= 30
                return "eats_stash"
            elif global_food > 0:
                return "steals_food" if self.psyche.conscientiousness < 0.3 else "begs_food"
            else:
                # CANNIBALISM TABOO BREAK
                if taboo_threshold > 80 and self.psyche.agreeableness < 0.2:
                    return "contemplates_cannibalism"

        # SOCIAL / POWER
        if self.psyche.extraversion > 0.7:
            return "agitates_crowd"

        # PASSIVE / SILENT MAJORITY
        return "observes"


# --- 2. SOCIAL NETWORK & POWER STRUCTURES ---

class SocialGraph:
    def __init__(self, agents: List[Agent]):
        self.graph = nx.Graph()
        self.agents_map = {a.uid: a for a in agents}

        # Initialize nodes
        for a in agents:
            self.graph.add_node(a.uid, label=a.name)

        # Initialize random relationships (Small World Network)
        # Some people know each other, creating clusters
        for a in agents:
            targets = random.sample(agents, k=random.randint(1, 4))
            for t in targets:
                if a != t:
                    weight = random.uniform(0.1, 1.0)  # Trust level
                    self.graph.add_edge(a.uid, t.uid, weight=weight)

    def update_metrics(self):
        """
        Runs Social Network Analysis (SNA) to find the 'Shadow Cabinet'.
        """
        # Betweenness Centrality: Who controls information flow? (The Broker)
        betweenness = nx.betweenness_centrality(self.graph)

        # Eigenvector Centrality: Who knows important people? (The Influencer)
        eigenvector = nx.eigenvector_centrality(self.graph, max_iter=500)

        shadow_leader = None
        max_score = -1

        for uid, score in eigenvector.items():
            agent = self.agents_map[uid]
            agent.influence_score = score
            if score > max_score and agent.role != "Captain":
                max_score = score
                shadow_leader = agent

        return shadow_leader

    def spread_rumor(self, source_agent: Agent, rumor_strength: float):
        """
        Viral Spread Mechanism.
        Rumors spread through edges. High extraversion agents amplify it.
        """
        infected_count = 0
        neighbors = list(self.graph.neighbors(source_agent.uid))
        for n_id in neighbors:
            neighbor = self.agents_map[n_id]
            # Transmission probability
            prob = rumor_strength * (1.0 - neighbor.psyche.openness)  # Closed minds believe rumors easier?
            if random.random() < prob:
                neighbor.radicalization += 2
                infected_count += 1
        return infected_count


# --- 3. THE SIMULATION ENGINE ---

class Simulation:
    def __init__(self):
        self.console = Console()
        self.turn = 0

        # Environmental Variables
        self.ship_heading_north = 0.0  # Doom meter
        self.food_supply = INITIAL_RESOURCES
        self.hull_integrity = 100.0

        # Sociological Variables
        self.overton_window = 0.0  # 0 = Civilized, 100 = Hobbesian Nightmare
        self.chaos_level = 0.0

        # Initialize Population
        roles = ["Captain", "Mate", "Boatswain", "Cook", "Doctor"] + ["Sailor"] * 5 + ["Passenger"] * 5
        self.agents = [Agent(i, f"{r}-{i}", r) for i, r in enumerate(roles)]

        self.network = SocialGraph(self.agents)
        self.logs = []
        self.shadow_leader = None

    def log(self, text, style="white"):
        self.logs.append(Text(f"T{self.turn}: {text}", style=style))
        if len(self.logs) > 15: self.logs.pop(0)

    def trigger_black_swan(self):
        """Random high-impact events."""
        roll = random.random()
        if roll < 0.05:
            self.log("BLACK SWAN: The Generator Explodes! (Chaos +20)", "bold red reverse")
            self.hull_integrity -= 15
            self.chaos_level += 20
        elif roll < 0.10:
            self.log("EVENT: Someone found a crate of Rum. (Moral Decay +10)", "yellow")
            self.overton_window += 10
            # Drunkenness reduces agreeableness globally
            for a in self.agents: a.psyche.agreeableness -= 0.1

    def run_turn(self):
        self.turn += 1
        self.ship_heading_north += 1.5
        self.food_supply -= len(self.agents) * 0.5

        # 1. Structural Decay
        if self.food_supply < 50: self.overton_window += 1
        if self.hull_integrity < 50: self.chaos_level += 1

        # 2. Network Analysis
        self.shadow_leader = self.network.update_metrics()

        # 3. Agent Actions
        actions_summary = {"theft": 0, "protest": 0, "violence": 0}

        for agent in self.agents:
            # Hunger increases naturally
            agent.hunger += random.uniform(1, 5)

            # Decide Action
            action = agent.decide_action(self.food_supply, self.overton_window)

            # Process Actions
            if action == "steals_food":
                if self.food_supply > 0:
                    self.food_supply -= 1
                    agent.hunger -= 10
                    actions_summary["theft"] += 1

            elif action == "agitates_crowd":
                spread = self.network.spread_rumor(agent, 0.4)
                actions_summary["protest"] += 1

            elif action == "contemplates_cannibalism":
                self.log(f"TABOO: {agent.name} is looking at the Cabin Boy hungrily...", "bold magenta")
                self.overton_window += 5  # Massive moral decay

            # Check for Scapegoating
            reaction = agent.react_to_event(self.chaos_level / 10, self.overton_window)
            if reaction: self.log(reaction, "dim red")

        # 4. Global Consequences
        if actions_summary["theft"] > 2:
            self.log(f"CRIME WAVE: {actions_summary['theft']} food thefts reported.", "red")
            self.overton_window += 2  # Normalization of crime

        if actions_summary["protest"] > 3:
            self.log(f"UNREST: {actions_summary['protest']} agitators screaming propaganda.", "yellow")
            self.chaos_level += 2

        self.trigger_black_swan()

    # --- VISUALIZATION LAYERS ---

    def render_ui(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["body"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=2)
        )

        # HEADER
        header_text = f"SIMULATION: SHIP OF FOOLS | Turn {self.turn} | Pop: {len(self.agents)}"
        layout["header"].update(Panel(header_text, style="white on blue"))

        # LEFT COLUMN: METRICS & SNA

        # 1. Overton Window (Moral Decay)
        overton_bar = Progress(
            TextColumn("[bold magenta]MORAL DECAY (Overton Window)"),
            BarColumn(bar_width=None, complete_style="magenta", finished_style="bold magenta"),
            TextColumn("{task.percentage:.0f}%")
        )
        overton_bar.add_task("", total=100, completed=self.overton_window)

        # 2. Ship Integrity
        doom_bar = Progress(
            TextColumn("[bold cyan]DISTANCE TO NORTH (Doom)"),
            BarColumn(bar_width=None, complete_style="cyan"),
            TextColumn("{task.percentage:.0f}%")
        )
        doom_bar.add_task("", total=100, completed=self.ship_heading_north)

        # 3. Network Intel (The Hidden Power)
        sna_table = Table(box=box.SIMPLE, title="SNA: Informal Power Structure")
        sna_table.add_column("Agent")
        sna_table.add_column("Influence (Centrality)")
        sna_table.add_column("Psyche")

        # Sort by influence
        sorted_agents = sorted(self.agents, key=lambda x: x.influence_score, reverse=True)[:5]
        for a in sorted_agents:
            is_shadow = " [Shadow Leader]" if a == self.shadow_leader else ""
            psyche_desc = "Neurotic" if a.psyche.neuroticism > 0.7 else "Stable"
            sna_table.add_row(
                f"{a.name}{is_shadow}",
                f"{a.influence_score:.3f}",
                psyche_desc
            )

        # Combine Left Panel
        left_layout = Layout()
        left_layout.split_column(
            Layout(Panel(overton_bar, title="Sociological Indicators")),
            Layout(Panel(doom_bar, title="Physical Indicators")),
            Layout(Panel(sna_table, title="Network Intelligence"))
        )
        layout["left"].update(left_layout)

        # RIGHT COLUMN: LOGS & AGENT STATES
        log_panel = Panel(Text("\n").join(self.logs), title="Live Event Feed", border_style="white")

        # Detailed Agent Matrix (Heatmap style)
        matrix_table = Table(box=box.SIMPLE_HEAD, show_edge=False, expand=True)
        matrix_table.add_column("ID", width=4)
        matrix_table.add_column("Role", width=10)
        matrix_table.add_column("Hunger")
        matrix_table.add_column("Radicalization")
        matrix_table.add_column("Trauma")

        for a in self.agents:
            h_style = "red" if a.hunger > 50 else "green"
            r_style = "red" if a.radicalization > 50 else "dim white"
            t_style = "yellow" if a.trauma > 50 else "dim white"

            matrix_table.add_row(
                str(a.uid),
                a.role,
                f"[{h_style}]{a.hunger:.0f}%[/]",
                f"[{r_style}]{a.radicalization:.0f}%[/]",
                f"[{t_style}]{a.trauma:.0f}%[/]"
            )

        right_layout = Layout()
        right_layout.split_column(
            Layout(log_panel, ratio=1),
            Layout(Panel(matrix_table, title="Psychological Monitor"), ratio=2)
        )
        layout["right"].update(right_layout)

        # FOOTER
        status = "CRITICAL" if self.overton_window > 80 else "STABLE"
        footer_panel = Panel(f"SYSTEM STATUS: {status} | Food Reserves: {self.food_supply:.0f}",
                             style="bold white on black")
        layout["footer"].update(footer_panel)

        return layout

    def start(self):
        with Live(self.render_ui(), refresh_per_second=4, screen=True) as live:
            while self.ship_heading_north < 100 and self.hull_integrity > 0:
                self.run_turn()
                live.update(self.render_ui())
                time.sleep(GAME_SPEED)

            # End State
            final_msg = Panel("SIMULATION ENDED\nThe Ship has either sunk or society has collapsed.",
                              style="bold red on white")
            live.update(final_msg)
            time.sleep(5)


if __name__ == "__main__":
    sim = Simulation()
    sim.start()