import argparse
import sys
from codeshuttle import CodeShuttle

def main():
    parser = argparse.ArgumentParser(description="CodeShuttle: Streamline code transfers between AI assistants and source files.")
    parser.add_argument("--input", required=True, help="Path to the input file containing the changes. Use '-' for stdin or 'pb' for clipboard.")
    parser.add_argument("--root", default=".", help="Root directory where changes will be applied. Defaults to current directory.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("--output", help="Specify a file to write the complete list of applied changes.")

    args = parser.parse_args()

    code_shuttle = CodeShuttle()
    try:
        code_shuttle.run(args.input, args.root, args.verbose, args.output)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()