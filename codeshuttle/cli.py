### FILE_PATH: codeshuttle/cli.py
import argparse
import sys
from codeshuttle import CodeShuttle, __version__

def apply_command(args):
    code_shuttle = CodeShuttle()
    try:
        code_shuttle.apply_changes(args.input, args.root, args.verbose, args.output, args.dry_run)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

def collect_command(args):
    code_shuttle = CodeShuttle()
    try:
        code_shuttle.collect_files(args.output, args.root, args.files, args.dry_run, args.verbose)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="CodeShuttle: Streamline code transfers between AI assistants and source files.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")
    parser.add_argument('--version', action='version', version=f'CodeShuttle {__version__}')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Apply subcommand
    apply_parser = subparsers.add_parser('apply', help='Apply changes from a diff file')
    apply_parser.add_argument('-i', '--input', required=True, help="Path to the input file containing the changes. Use '-' for stdin or 'pb' for clipboard.")
    apply_parser.add_argument('-r', '--root', default=".", help="Root directory where changes will be applied. Defaults to current directory.")
    apply_parser.add_argument('-o', '--output', help="Specify a file to write the complete list of applied changes.")
    apply_parser.add_argument('-d', '--dry-run', action='store_true', help="Preview changes without applying them")
    apply_parser.set_defaults(func=apply_command)

    # Collect subcommand
    collect_parser = subparsers.add_parser('collect', help='Collect the state of multiple files into a context file')
    collect_parser.add_argument('-o', '--output', required=True, help="Output file to write the context")
    collect_parser.add_argument('-r', '--root', default=".", help="Root directory to start scanning files. Defaults to current directory.")
    collect_parser.add_argument('-f', '--files', help="File with list of patterns for including and excluding files for collection")
    collect_parser.add_argument('-d', '--dry-run', action='store_true', help="Preview files that would be included without generating the output")
    collect_parser.set_defaults(func=collect_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()