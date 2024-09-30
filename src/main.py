from baseline.core import Above50, Evaluation, Selector
from projects.mvp.random_service import RandomService, generate_dataset

if __name__ == "__main__":
    dataset = generate_dataset()

    selector = Selector()

    evaluators = [Above50()]

    evaluation = Evaluation(
        dataset, selector, evaluators, callback=RandomService.generate
    )

    evaluation.run()

    for outcome in evaluation.outcomes:
        print(outcome.data.value, outcome.value, len(outcome.properties))
