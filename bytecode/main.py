import tempfile
import zipfile
from pathlib import Path
from pprint import pprint

from bytecode.score import load_score


def extract_zip(zip_file: Path) -> Path:
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        temp_dir = Path(tempfile.mkdtemp())
        zip_ref.extractall(temp_dir)
        for file in temp_dir.rglob('*.mscx'):
            return file
    raise FileNotFoundError("No .mscx file found in the zip archive")


def main(input_file: Path, output_file: Path):
    object_score = load_score(input_file)
    pprint(object_score)
    output_file.write_text(object_score.serialize())
