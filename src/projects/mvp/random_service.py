import random
import time

from baseline.core import Data, Dataset


def generate_dataset(n=10) -> Dataset:
    random.seed(int(time.time() * 1000))

    return Dataset(
        [Data(value=random.randint(0, 100), properties=["test"]) for _ in range(n)]
    )


class RandomService:
    @staticmethod
    def generate(seed: int):
        random.seed(seed)
        return random.randint(0, 100)
