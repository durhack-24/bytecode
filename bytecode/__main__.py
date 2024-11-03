import shutil
from pathlib import Path


if __name__ == "__main__":
    import sys
    from bytecode import main

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists() or not input_file.is_file():
        print("Input file does not exist or is not a file")
        sys.exit(1)

    if input_file.suffix not in [".xml", ".mscx", ".mscz", ".zip"]:
        print("Input file must be a xml file")
        sys.exit(1)

    is_tmp = False

    if input_file.suffix in [".zip", ".mscz"]:
        is_tmp = True
        input_file = main.extract_zip(input_file)

    out = main.main(input_file, output_file)

    if is_tmp:
        shutil.rmtree(input_file.parent)

    sys.exit(out)
