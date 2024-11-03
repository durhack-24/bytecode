from dataclasses import dataclass


@dataclass
class Value:
    tick: int
    value: int


@dataclass
class Operation(Value):
    # value is diff between two notes

    def serialize(self):
        return f"O{abs(self.value)}\n"


@dataclass
class Datum(Value):
    # value is diff between two notes
    def serialize(self):
        return f"D{self.value}\n"


@dataclass
class Variable(Value):
    # value is note value is the name of a variable
    def serialize(self):
        return f"V{self.value}\n"


@dataclass
class Label(Value):
    # label is a practice mark
    value: str

    def serialize(self):
        return f"L{self.value}\n"


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

    @staticmethod
    def __remove_nop_data(input):
        # remove everything between a noop instruction and the next instruction
        output = []
        last_is_noop = False
        noop_instruction = "O0"
        for line in input:
            if line[2][0] == noop_instruction:
                last_is_noop = True
            elif last_is_noop and line[2][0] == noop_instruction:
                last_is_noop = False
            else:
                output.append(line)
        return output








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
        output = self.__remove_nop_data(output)
        return "".join(x[2] for x in output)
