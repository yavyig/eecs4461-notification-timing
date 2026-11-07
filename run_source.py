"""Run the preserved local source files without modifying their upstream imports."""

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent / "src" / "boltzmann_wealth_model"


def load_local(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


load_local("mesa.examples.basic.boltzmann_wealth_model.agents", "agents.py")
source = load_local("preserved_boltzmann_model", "model.py")
model = source.BoltzmannWealth(source.BoltzmannScenario(n=100, width=10, height=10))
for _ in range(10):
    model.step()
assert sum(agent.wealth for agent in model.agents) == 100
assert all(agent.wealth >= 0 for agent in model.agents)
print(f"Preserved source completed 10 steps; agents=100; total wealth=100; Gini={model.gini:.4f}")
