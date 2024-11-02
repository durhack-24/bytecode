from dataclasses import dataclass


@dataclass
class Value:
    tick: int
    value: int


@dataclass
class Operation(Value):
    # value is diff between two notes

    def serialize(self):
        return (f"{self.tick}O{self.value}\n")


@dataclass
class Datum(Value):
    # value is diff between two notes
    def serialize(self):
        return (f"{self.tick}D{self.value}\n")

@dataclass
class Variable(Value):
    # value is note value is the name of a variable
    def serialize(self):
        return (f"{self.tick}V{self.value}\n")


@dataclass
class Label(Value):
    # label is a practice mark
    value: str

    def serialize(self):
        return (f"{self.tick}L{self.value}\n")


@dataclass
class Score:
    operations: list[Operation]
    data: list[Datum]
    variables: list[Variable]
    labels: list[Label]

    def merge(self, other):
        self.operations.extend(other.operations)
        self.data.extend(other.data)
        self.variables.extend(other.variables)
        self.labels.extend(other.labels)
        return self

    def serialize(self):
        output = []
        for operation in self.operations:
            output.append((operation.tick, 1, operation.serialize()))

        for datum in self.data:
            output.append((datum.tick, 2, datum.serialize()))

        for variable in self.variables:
            output.append((variable.tick, 3, variable.serialize()))

        for label in self.labels:
            output.append((label.tick, 0, label.serialize()))

        output.sort()
        return "".join(x[2] for x in output)