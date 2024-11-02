import xml.etree.ElementTree as ET
from pathlib import Path

from .main import Score as ObjectScore, Label, Variable, Datum, Operation
from .muse import Score as MuseScore


def interval_evaluator(staff, staff_name, ValueType):
    values: list[ValueType] = []

    notes = staff.get_notes()
    if len(notes) == 0:
        raise SyntaxError("No notes found in score for " + staff_name)
    clock = 0
    last_note = None
    note_counter = 0
    for note in notes:
        if note.pitch == -1:
            values.append(ValueType(clock, 0))
            last_note = None
            clock += note.duration
            continue

        if last_note is not None:
            # get diff between this and previous
            diff = note.pitch - last_note.pitch
            values.append(ValueType(clock, diff))

            clock += note.duration + last_note.duration
            last_note = None
        else:
            last_note = note

        note_counter += 1
    return values


def get_operations(muse_score: MuseScore) -> list[Operation]:
    staff = muse_score.staffs[0]
    staff_name = "operations"
    return interval_evaluator(staff, staff_name, Operation)


def get_data(muse_score: MuseScore) -> list[Datum]:
    staff = muse_score.staffs[1]
    staff_name = "data"
    # TODO fix None types
    return []#interval_evaluator(staff, staff_name, Datum)


def get_variables(muse_score: MuseScore) -> list[Variable]:
    variables = []
    # TODO implement

    return variables


def get_labels(muse_score: MuseScore) -> list[Label]:
    labels = []
    # TODO implement
    # for child in muse_score:
    #     if child.tag == "Labels":
    #         for grand_child in child:
    #             labels.append(grand_child.text)
    return labels


def muse_to_object(muse_score: MuseScore) -> ObjectScore:
    operations = get_operations(muse_score)
    data = get_data(muse_score)
    variables = get_variables(muse_score)
    labels = get_labels(muse_score)
    return ObjectScore(operations, data, variables, labels)


def load_score(score_path: Path) -> ObjectScore | None:
    with open(score_path, 'r') as f:
        score_str = f.read()
    score_xml = ET.fromstring(score_str)
    muse_score = None
    for child in score_xml:
        if child.tag == "Score":
            muse_score = MuseScore(child)
    if muse_score is None:
        return None

    return muse_to_object(muse_score)
