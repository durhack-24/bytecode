import xml.etree.ElementTree as ET
from pathlib import Path

from .main import Score as ObjectScore, Label, Variable, Datum, Operation
from .muse import Score as MuseScore


def get_operations(muse_score: MuseScore) -> list[Operation]:
    operations = []
    # TODO implement
    # for child in muse_score:
    #     if child.tag == "Operations":
    #         for grand_child in child:
    #             operations.append(grand_child.text)
    return operations


def get_data(muse_score: MuseScore) -> list[Datum]:
    data = []
    # TODO implement
    # for child in muse_score:
    #     if child.tag == "Data":
    #         for grand_child in child:
    #             data.append(grand_child.text)
    return data


def get_variables(muse_score: MuseScore) -> list[Variable]:
    variables = []
    # TODO implement
    # for child in muse_score:
    #     if child.tag == "Variables":
    #         for grand_child in child:
    #             variables.append(grand_child.text)
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
