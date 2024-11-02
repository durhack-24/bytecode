from pathlib import Path
from pprint import pprint

from bytecode.score import load_score


def main(input_file: Path, output_file: Path):
    object_score = load_score(input_file)
    pprint(object_score)
    output_file.write_text(object_score.serialize())
