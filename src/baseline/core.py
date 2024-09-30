from typing import Any, Callable, List


class Expander:
    pass


class Selector:
    pass


class Data:
    def __init__(self, properties: List[str], value: Any):
        self.properties = properties
        self.value = value


class Dataset:
    def __init__(self, dataset: List[Data]):
        self.dataset = dataset


class Outcome:
    def __init__(self, data: Data, value: Any):
        self.properties = []
        self.properties.extend(data.properties)

    def add_property(self, property: str):
        self.properties.append(property)


class Evaluator:
    def eval(data: Data, outcome: Outcome):
        pass


class Simulation:
    def __init__(
        self,
        data: Data,
        evaluators: List[Evaluator],
        callback: Callable[[], Any],
        num_runs: int = 10,
    ):
        self.data = data
        self.evaluators = evaluators
        self.callback = callback
        self.num_runs = num_runs
        self.outcomes: List[Outcome] = []

    def run(self):
        for _ in range(self.num_runs):
            self.outcomes.append(
                Outcome(data=self.data, value=self.callback(self.data.value))
            )

        return self.outcomes


class Evaluation:
    def __init__(
        self,
        dataset: Dataset,
        selector: Selector,
        evaluators: List[Evaluator],
        callback: Callable[[Any], Any],
    ):
        self.selector = selector
        self.simulations: List[Simulation] = [
            Simulation(data=data, callback=callback, evaluators=evaluators)
            for data in dataset.dataset
        ]
        self.outcomes: List[Outcome] = []

    def run(self):
        for simulation in self.simulations:
            self.outcomes.extend(simulation.run())

        print(len(self.outcomes))
