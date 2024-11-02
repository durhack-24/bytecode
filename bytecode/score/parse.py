import xml.etree.ElementTree as ET
from pathlib import Path

from .muse import Score


def load_score(score_path: Path) -> Score:
    with open(score_path, 'r') as f:
        score_str = f.read()
    score_xml = ET.fromstring(score_str)
    for child in score_xml:
        if child.tag == "Score":
            return Score(child)
    return None
