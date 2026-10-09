"""Shared, finite resource pool for the ship (food & water)."""


class ResourcePool:
    def __init__(self, food: float, water: float, capacity: float,
                 food_regen_rate: float, water_regen_rate: float):
        self.food = food
        self.water = water
        self.capacity = capacity
        self.food_regen_rate = food_regen_rate
        self.water_regen_rate = water_regen_rate

    def regenerate(self):
        self.food = min(self.capacity, self.food + self.food_regen_rate * self.capacity)
        self.water = min(self.capacity, self.water + self.water_regen_rate * self.capacity)

    def true_scarcity(self) -> float:
        """0 = full capacity, 1 = empty — the ground truth agents only perceive noisily."""
        level = (self.food + self.water) / (2 * self.capacity)
        return 1 - level

    def take(self, kind: str, amount: float) -> float:
        stock = self.food if kind == "food" else self.water
        got = min(stock, amount)
        if kind == "food":
            self.food -= got
        else:
            self.water -= got
        return got

    def add(self, kind: str, amount: float):
        if kind == "food":
            self.food = min(self.capacity, self.food + amount)
        else:
            self.water = min(self.capacity, self.water + amount)
