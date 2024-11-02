from dataclasses import dataclass


@dataclass
class Value:
    tick: int
    value: int


@dataclass
class Operation(Value):
    # value is diff between two notes
    pass


@dataclass
class Datum(Value):
    # value is diff between two notes
    pass


@dataclass
class Variable(Value):
    # value is note value is the name of a variable
    pass


@dataclass
class Label(Value):
    # label is a practice mark
    value: str


@dataclass
class Score:
    operations: list[Operation]
    data: list[Datum]
    variables: list[Variable]
    labels: list[Label]
