"""Smoke checks for the alternative action schedule."""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ship_of_fools.configuration.config import Config
from ship_of_fools.simulation.engine import Simulation


class ScheduleRobustnessTests(unittest.TestCase):
    def test_shuffled_schedule_repeats_for_same_seed(self):
        config = Config(n_agents=12, n_ticks=8, seed=719, agent_update_order="shuffled")
        first = Simulation(config).run().to_rows()
        second = Simulation(config).run().to_rows()
        self.assertEqual(first, second)

    def test_invalid_schedule_is_rejected(self):
        config = Config(n_agents=12, n_ticks=1, seed=719, agent_update_order="invalid")
        with self.assertRaises(ValueError):
            Simulation(config).run()

    def test_per_agent_rng_mode_repeats(self):
        config = Config(n_agents=12, n_ticks=8, seed=811, agent_update_order="shuffled",
                        agent_rng_mode="per_agent")
        first = Simulation(config).run().to_rows()
        second = Simulation(config).run().to_rows()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
