from abc import ABC
from typing import Any, Callable, List


class Data:
    def __init__(self, properties: List[str], value: Any):
        self.properties = properties
        self.value = value


class Expander(ABC):
    def __init__(self, data: Data):
        pass

    def expand(self):
        pass


class Dataset:
    def __init__(self, dataset: List[Data]):
        self.dataset = dataset


class Selector(ABC):
    def select():
        pass


class Outcome:
    def __init__(self, data: Data, value: Any):
        self.data = data
        self.value = value
        self.properties = []
        self.properties.extend(data.properties)

    def add_property(self, _property: str):
        self.properties.append(_property)


class Evaluator(ABC):
    def __init__(self, _property: str):
        pass

    def eval(self, outcome: Outcome) -> bool:
        pass


class Simulation:
    def __init__(
        self,
        data: Data,
        evaluators: List[Evaluator],
        callback: Callable[[], Any],
        num_runs: int = 1,
    ):
        self.data = data
        self.evaluators = evaluators
        self.callback = callback
        self.num_runs = num_runs
        self.outcomes: List[Outcome] = []

    def run(self):
        for i in range(self.num_runs):
            print("run ", i)
            outcome = Outcome(data=self.data, value=self.callback(self.data.value))

            for expander in self.evaluators:
                expander.eval(outcome)

            self.outcomes.append(outcome)

        return self.outcomes


class Evaluation:
    def __init__(
        self,
        dataset: Dataset,
        # selector: Selector,
        evaluators: List[Evaluator],
        callback: Callable[[Any], Any],
    ):
        # self.selector = selector
        self.simulations: List[Simulation] = [
            Simulation(data=data, callback=callback, evaluators=evaluators)
            for data in dataset.dataset
        ]
        self.outcomes: List[Outcome] = []

    def run(self):
        i = 0
        for simulation in self.simulations:
            self.outcomes.extend(simulation.run())
            i += 1
