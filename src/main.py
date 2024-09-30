from baseline.core import Evaluation, Evaluator, Selector
from projects.mvp.random_service import RandomService, generate_dataset

if __name__ == "__main__":
    dataset = generate_dataset()

    selector = Selector()

    evaluators = [Evaluator()]

    evaluation = Evaluation(
        dataset, selector, evaluators, callback=RandomService.generate
    )

    evaluation.run()
