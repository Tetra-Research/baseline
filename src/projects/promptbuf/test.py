from enum import Enum
import json
from typing import Any
from baseline.core import Data, Dataset, Evaluation, Evaluator, Outcome
from .lib_cpy import encode, decode


class ValidJSON(Evaluator):
    def __init__(self):
        self.property = "valid_json"

    def eval(self, outcome: Outcome):
        try:
            json.loads(json.dumps(outcome.value))
            outcome.add_property(self.property)
        except Exception as e:
            print("exception1", e)
            return


class AccurateJSON(Evaluator):
    def __init__(self):
        self.property = "accurate_json"

    def eval(self, outcome: Outcome) -> bool:
        try:
            is_match = json.dumps(outcome.data.value[0]) == json.dumps(outcome.value)

            if is_match:
                outcome.add_property(self.property)

        except Exception as e:
            print("exception1", e)
            return


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


def run():
    evaluators = [ValidJSON(), AccurateJSON()]

    dataset = Dataset(
        dataset=[
            # Primitives
            Data(value=(1, {"type": "integer"}), properties=["primitive", "integer"]),
            Data(value=(15, {"type": "integer"}), properties=["primitive", "integer"]),
            Data(value=(1.5, {"type": "number"}), properties=["primitive", "number"]),
            Data(value=(11.55, {"type": "number"}), properties=["primitive", "number"]),
            Data(
                value=("Test string", {"type": "string"}),
                properties=["primitive", "string"],
            ),
            Data(
                value=(True, {"type": "boolean"}), properties=["primitive", "boolean"]
            ),
            Data(value=(None, {"type": "null"}), properties=["primitive", "null"]),
            Data(
                value=(
                    Color.GREEN.value,
                    {"type": "string", "enum": ["red", "green", "blue"]},
                ),
                properties=["primitive", "enum"],
            ),
            # Arrays
            Data(
                value=([1, 2], {"type": "array", "items": {"type": "integer"}}),
                properties=["array", "integer"],
            ),
            Data(
                value=([11, 22], {"type": "array", "items": {"type": "integer"}}),
                properties=["array", "integer"],
            ),
            Data(
                value=([1.5, 2.5], {"type": "array", "items": {"type": "number"}}),
                properties=["array", "number"],
            ),
            Data(
                value=([11.55, 22.55], {"type": "array", "items": {"type": "number"}}),
                properties=["array", "number"],
            ),
            Data(
                value=(
                    ["test", "string"],
                    {"type": "array", "items": {"type": "string"}},
                ),
                properties=["array", "string"],
            ),
            Data(
                value=(
                    [Color.BLUE.value, Color.GREEN.value, Color.RED.value],
                    {
                        "type": "array",
                        "items": {"type": "string", "enum": ["red", "green", "blue"]},
                    },
                ),
                properties=["array", "enum"],
            ),
            # Objects
            Data(
                value=(
                    {"name": "Tyler", "age": 29, "isEnabled": True},
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer"},
                            "isEnabled": {"type": "boolean"},
                        },
                    },
                ),
                properties=["object", "string", "number", "boolean"],
            ),
            Data(
                value=(
                    {
                        "name": "Tyler",
                        "age": 29,
                        "isEnabled": False,
                        "ids": [1, 2, 3, 4, 5],
                    },
                    {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "integer"},
                            "isEnabled": {"type": "boolean"},
                            "ids": {"type": "array", "items": {"type": "integer"}},
                        },
                    },
                ),
                properties=["object", "array", "boolean", "integer", "string"],
            ),
            Data(
                value=(
                    {"age": 29, "isEnabled": True},
                    {
                        "type": "object",
                        "properties": {
                            "age": {"type": "integer"},
                            "isEnabled": {"type": "boolean"},
                        },
                    },
                ),
                properties=["object", "integer", "boolean"],
            ),
            Data(
                value=(
                    {"name": {"first": "Tyler", "last": "O'Briant"}},
                    {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "object",
                                "properties": {
                                    "first": {"type": "string"},
                                    "last": {"type": "string"},
                                },
                            },
                        },
                    },
                ),
                properties=["object", "nested_1", "string"],
            ),
            Data(
                value=(
                    {
                        "name": {"first": "Tyler", "last": "O'Briant"},
                        "age": 29,
                        "isEnabled": True,
                    },
                    {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "object",
                                "properties": {
                                    "first": {"type": "string"},
                                    "last": {"type": "string"},
                                },
                            },
                            "age": {"type": "integer"},
                            "isEnabled": {"type": "boolean"},
                        },
                    },
                ),
                properties=["object", "nested_1", "boolean", "age", "string"],
            ),
            Data(
                value=(
                    {"ids": [1, 2, 3, 4, 5], "age": 29, "isEnabled": False},
                    {
                        "type": "object",
                        "properties": {
                            "ids": {
                                "type": "array",
                                "items": {"type": "integer"},
                            },
                            "age": {"type": "integer"},
                            "isEnabled": {"type": "boolean"},
                        },
                    },
                ),
                properties=["object", "array", "integer", "boolean", "primitive"],
            ),
        ]
    )

    def promptbuf(v: Any):
        return decode(encode(v[0], v[1]), v[1])

    evaluation = Evaluation(dataset, evaluators, callback=promptbuf)

    evaluation.run()

    for i in range(int(len(evaluation.outcomes) / 10)):
        outcome = evaluation.outcomes[(i * 10)]
        print(
            "valid_json" in outcome.properties
            and "accurate_json" in outcome.properties,
        )
