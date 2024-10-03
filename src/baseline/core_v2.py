from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
from typing import Callable, Generic, List, TypeVar

T = TypeVar("T")
V = TypeVar("V")


@dataclass
class Data(Generic[T]):
    value: T
    properties: List[str]


class Expander(ABC):
    property: str = ""

    @abstractmethod
    def expand(self, data: Data) -> Data: ...


class Selector(ABC):
    @staticmethod
    @abstractmethod
    def select(self, dataset: List[Data]) -> List[Data]: ...


class CoinFlipSelector(Selector):
    def select(self, dataset: List[Data]) -> List[Data]:
        return [d for d in dataset if random.choice([True, False])]


class AddOneExpander(Expander):
    property = "added_one"

    def expand(self, data: Data) -> Data:
        cpy = Data(value=data.value + 1, properties=data.properties)
        cpy.properties.append(property)

        return cpy


@dataclass
class Outcome(Generic[V]):
    value: V
    properties: List[str]


@dataclass
class SimulationRun(Generic[T, V]):
    data: Data[T]
    outcome: Outcome[V]


class Evaluator(ABC):
    property: str = ""

    @abstractmethod
    def eval(self, outcome: Outcome) -> None: ...


class MultipleOf2Evaluator(Evaluator):
    property = "multiple_of_2"

    def eval(self, outcome: Outcome):
        if outcome.value % 2 == 0:
            outcome.properties.append(self.property)


class Simulation(Generic[T, V]):
    def __init__(
        self,
        data: Data[T],
        callback: Callable[[T], V],
        evaluators: List[Evaluator],
        num_runs: int,
    ):
        self.data = data
        self.callback = callback
        self.evaluators = evaluators

        self.runs: List[SimulationRun[T, V]] = []
        self.num_runs = num_runs

    def run(self):
        for i in range(self.num_runs):
            outcome = Outcome(value=self.callback(self.data.value), properties=[])

            for expander in self.evaluators:
                expander.eval(outcome)

            print("Run ", i, self.data.value, outcome.value, len(outcome.properties))
            self.runs.append(SimulationRun(self.data, outcome))

        return self.runs


class Evaluation(Generic[T, V]):
    def __init__(
        self,
        dataset: List[Data[T]],
        callback: Callable[[T], V],
        evaluators: List[Evaluator],
        num_simulation_runs=10,
    ):
        self.dataset = dataset
        self.callback = callback
        self.evaluators = evaluators

        self.simulations: List[Simulation] = [
            Simulation[T, V](data, callback, evaluators, num_simulation_runs)
            for data in dataset
        ]

        self.results: List[SimulationRun] = []

    def run(self):
        for i, simulation in enumerate(self.simulations):
            print("Running simulation: ", i)
            self.results.extend(simulation.run())


def add_ten_cb(v: int):
    return v + 10


dataset = [
    Data[int](value=1, properties=["below_ten"]),
    Data[int](value=11, properties=["above_ten"]),
]

dataset.extend([AddOneExpander().expand(d) for d in dataset])

eval = Evaluation[int, int](dataset, add_ten_cb, [MultipleOf2Evaluator()], 50)

eval.run()
# print(eval.results)
