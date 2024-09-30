from baseline.core import Evaluation, Evaluator, Outcome, Selector
from projects.mvp.random_service import RandomService, generate_dataset


class Above50(Evaluator):
    def __init__(self):
        self.property = "above_50"

    def eval(self, outcome: Outcome):
        if outcome.value > 50:
            outcome.add_property(self.property)


def run():
    dataset = generate_dataset()

    evaluators = [Above50()]

    evaluation = Evaluation(dataset, evaluators, callback=RandomService.generate)

    evaluation.run()

    for outcome in evaluation.outcomes:
        print(outcome.data.value, outcome.value, len(outcome.properties))
