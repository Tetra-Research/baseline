from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, List, TypeVar

DataType = TypeVar("DataType")
OutcomeType = TypeVar("OutcomeType")


@dataclass
class Data(Generic[DataType]):
    value: DataType
    properties: List[str]


class Expander(ABC):
    property: str = ""

    @abstractmethod
    def expand(self, data: Data) -> Data: ...


class Selector(ABC):
    @staticmethod
    @abstractmethod
    def select(self, dataset: List[Data]) -> List[Data]: ...


@dataclass
class Outcome(Generic[OutcomeType]):
    value: OutcomeType
    properties: List[str]


@dataclass
class SimulationRun(Generic[DataType, OutcomeType]):
    data: Data[DataType]
    outcome: Outcome[OutcomeType]


class Evaluator(ABC):
    property: str = ""

    @abstractmethod
    def eval(self, outcome: Outcome) -> None: ...


class Simulation(Generic[DataType, OutcomeType]):
    def __init__(
        self,
        data: Data[DataType],
        callback: Callable[[DataType], OutcomeType],
        evaluators: List[Evaluator],
        num_runs: int,
    ):
        self.data = data
        self.callback = callback
        self.evaluators = evaluators

        self.runs: List[SimulationRun[DataType, OutcomeType]] = []
        self.num_runs = num_runs

    def run(self):
        for _ in range(self.num_runs):
            outcome = Outcome(value=self.callback(self.data.value), properties=[])

            for expander in self.evaluators:
                expander.eval(outcome)

            self.runs.append(SimulationRun(self.data, outcome))

        return self.runs


class Evaluation(Generic[DataType, OutcomeType]):
    def __init__(
        self,
        dataset: List[Data[DataType]],
        callback: Callable[[DataType], OutcomeType],
        evaluators: List[Evaluator],
        num_simulation_runs=10,
    ):
        self.dataset = dataset
        self.callback = callback
        self.evaluators = evaluators

        self.simulations: List[Simulation] = [
            Simulation[DataType, OutcomeType](
                data, callback, evaluators, num_simulation_runs
            )
            for data in dataset
        ]

        self.results: List[SimulationRun] = []

    def run(self):
        for simulation in self.simulations:
            self.results.extend(simulation.run())
