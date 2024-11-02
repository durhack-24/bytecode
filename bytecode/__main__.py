from pathlib import Path

if __name__ == "__main__":
    import sys
    from bytecode import main
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists() or not input_file.is_file():
        print("Input file does not exist or is not a file")
        sys.exit(1)

    if input_file.suffix != ".xml":
        print("Input file must be a xml file")
        sys.exit(1)

    sys.exit(main.main(input_file, output_file))
