import random
import time

from baseline.core import Data, Dataset


def generate_dataset(n=10) -> Dataset:
    random.seed(int(time.time() * 1000))

    dataset = []

    for _ in range(n):
        value = random.randint(0, 100)
        properties = []
        if value < 50:
            properties.append("below_50")

        dataset.append(Data(value=value, properties=properties))

    return Dataset(dataset=dataset)


class RandomService:
    @staticmethod
    def generate(seed: int):
        random.seed(seed)
        return random.randint(0, 100)
