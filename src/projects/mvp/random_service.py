import random
import time
from typing import List

dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def generate_dataset(n=10) -> List[int]:
    []

    random.seed(int(time.time() * 1000))

    return [random.randint(0, 100) for _ in range(n)]


class RandomService:
    @staticmethod
    def generate(seed: int):
        random.seed(seed)
        return random.randint(0, 100)
