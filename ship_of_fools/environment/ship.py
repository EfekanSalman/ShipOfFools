"""The ship: the closed environment agents live in."""
import random
from ..economy.resources import ResourcePool


class Ship:
    def __init__(self, config, rng: random.Random):
        self.tick = 0
        self.rng = rng
        # Scale per-agent quantities by population so the regen/consumption
        # balance doesn't silently break when n_agents changes (see config.py).
        n = max(1, config.n_agents)
        self.resources = ResourcePool(
            food=config.initial_food_per_agent * n,
            water=config.initial_water_per_agent * n,
            capacity=config.resource_capacity_per_agent * n,
            food_regen_rate=config.food_regen_rate,
            water_regen_rate=config.water_regen_rate,
        )
        self.disaster_active = False
        self.disaster_shock = 0
        self.public_reserve = 0.0  # TASK-202: taxed wealth awaiting redistribution

    def step(self):
        self.tick += 1
        self.resources.regenerate()
        # rare random shock: a storm damages resources for a while (doc 1, section 7)
        if not self.disaster_active and self.rng.random() < 0.003:
            self.disaster_active = True
            self.disaster_shock = self.rng.randint(10, 30)
        if self.disaster_active:
            self.resources.food *= 0.995
            self.resources.water *= 0.995
            self.disaster_shock -= 1
            if self.disaster_shock <= 0:
                self.disaster_active = False
