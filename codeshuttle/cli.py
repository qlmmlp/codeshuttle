import argparse
from .codeshuttle import CodeShuttle

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply code changes based on a specified format.")
    parser.add_argument("--input", help="Input source. Can be file path, stdin, or 'pb' for clipboard. (use '-' for stdin)", required=True)
    parser.add_argument("--root", help="Root directory for applying changes", default=".")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def main():
    args = parse_arguments()
    shuttle = CodeShuttle()
    shuttle.run(args.input, args.root, args.verbose)

if __name__ == "__main__":
    main()