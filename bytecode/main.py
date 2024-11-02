from pathlib import Path

from bytecode.score import load_score


def main(input_file: Path, output_file: Path):
    object_score = load_score(input_file)
    print(object_score)
    output_file.write_text(object_score.serialize())
