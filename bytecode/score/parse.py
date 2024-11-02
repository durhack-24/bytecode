import xml.etree.ElementTree as ET
from pathlib import Path

from bytecode.score.main import Score, Value

durations = {
    "sixteenth": 1,
    "eighth": 2,
    "quarter": 4,
    "half": 8,
    "whole": 16
}


def parse_measure(measure_xml: ET.Element) -> list[Value]:
    print("############################### Bar")
    values = []
    for child in measure_xml:
        if child.tag == "voice":
            print("---------------------------- Voice")
            for child in child:
                if child.tag == "Chord":
                    tick = 0
                    pitches = []
                    for child in child:
                        if child.tag == "durationType":
                            tick = durations[child.text]
                        if child.tag == "Note":
                            for child in child:
                                if child.tag == "pitch":
                                    pitches.append(int(child.text))
                    print(tick, pitches)

    return values


def parse_staff(staff_xml: ET.Element) -> list[Value]:
    values = []
    for child in staff_xml:
        if child.tag == "Measure":
            values.extend(parse_measure(child))
    return values


def parse_score_children(score_xml: ET.Element) -> Score:
    score = Score([], [], [], [])
    for child in score_xml:
        if child.tag == "Staff":
            print("|||||||||||||||||||| Staff")
            score.operations = parse_staff(child)
    return score


def parse_score(score_xml: ET.Element) -> Score:
    operations = []
    data = []
    variables = []
    labels = []
    for child in score_xml:
        if child.tag == "Score":
            print(parse_score_children(child))

    return Score(operations, data, variables, labels)


def load_score(score_path: Path) -> Score:
    with open(score_path, 'r') as f:
        score_str = f.read()
    score_xml = ET.fromstring(score_str)
    return parse_score(score_xml)
