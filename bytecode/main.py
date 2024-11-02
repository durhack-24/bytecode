from pathlib import Path

from bytecode.score import load_score


def main():
    load_score(Path('./example_data/score.xml'))
