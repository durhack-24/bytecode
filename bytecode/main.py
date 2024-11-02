from pathlib import Path

from bytecode.score import load_score


def main():
    print(load_score(Path('./example_data/score.xml')))
