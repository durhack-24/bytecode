import xml.etree.ElementTree as ET
from pathlib import Path

from .main import Score as ObjectScore, Label, Variable, Datum, Operation
from .muse import Score as MuseScore, SlurState


def interval_evaluator(
        staff,
        staff_name,
        ValueType,
        ignore_rests=False,
        slur_accumulator=False
):
    values: list[ValueType] = []

    notes = staff.get_notes()
    if len(notes) == 0:
        raise SyntaxError("No notes found in score for " + staff_name)
    clock = 0
    last_note = None
    note_counter = 0
    accumulator = 0
    for note in notes:
        if note.pitch == -1:
            if not ignore_rests:
                values.append(ValueType(clock, 0))
            last_note = None
            clock += note.duration
            continue

        if last_note is not None:
            # get diff between this and previous
            diff = note.pitch - last_note.pitch
            if note.slur_state == SlurState.SLUR_START and slur_accumulator:
                accumulator = diff
                clock += note.duration
            elif note.slur_state == SlurState.NO_SLUR and slur_accumulator:
                # bit shift left by 4 to make room for next diff
                if accumulator == 0:
                    sign = (diff >> 31) & 1
                else:
                    sign = (accumulator >> 31) & 1

                # Apply the sign to the result
                accumulator = ((accumulator << 4) + diff) & 0xFFFFFFFF
                if sign:
                    accumulator = -accumulator
                clock += note.duration
            elif note.slur_state == SlurState.SLUR_END and slur_accumulator:
                values.append(ValueType(clock, accumulator))
                clock += note.duration
                last_note = None
                accumulator = 0
            else:
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
    return interval_evaluator(
        staff,
        staff_name,
        Datum,
        ignore_rests=True,
        slur_accumulator=True
    )


def get_variables(muse_score: MuseScore) -> list[Variable]:
    variables = []
    staff = muse_score.staffs[2]

    notes = staff.get_notes()
    clock = 0
    for note in notes:
        if note.pitch != -1:
            variables.append(Variable(clock, note.pitch))
        clock += note.duration

    return variables


def get_labels(muse_score: MuseScore) -> list[Label]:
    labels = []
    rehearsal_marks = muse_score.staffs[0].get_rehearsal_marks()
    for rehearsal_mark in rehearsal_marks:
        labels.append(Label(rehearsal_mark.ticks, rehearsal_mark.text))
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
