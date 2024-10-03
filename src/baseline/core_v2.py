from abc import ABC
from dataclasses import dataclass
from typing import Any, Callable, Generic, List, TypeVar

T = TypeVar("T")
V = TypeVar("V")


@dataclass
class Data(Generic[T]):
    value: T
    properties: List[str]


Dataclass = List[Data]


@dataclass
class Outcome(Generic[V]):
    value: V
    properties: List[str]


@dataclass
class SimulationRun(Generic[T, V]):
    data: Data[T]
    outcome: Outcome[V]

class Evaluator(ABC):
    


class Simulation(Generic[T, V]):
    def __init__(self, data: Data[T], callback: Callable[[T], V], num_runs: int):
        self.data = data
        self.callback = callback
        # self.outcomes: List[Outcome[V]] = []

        self.runs: List[SimulationRun[T, V]] = []
        self.num_runs = num_runs

    def run(self):
        for i in range(self.num_runs):
            print("run ", i)
            outcome = Outcome(value=self.callback(self.data.value), properties=[])

            # for expander in self.evaluators:
            # expander.eval(outcome)

            self.runs.append(SimulationRun(data, outcome))

        return self.runs


def add_ten_cb(v: int):
    return v + 10


data = Data[int](value=1, properties=["below_ten"])

sim = Simulation[int, int](data, add_ten_cb, 50)

print(sim.run())
