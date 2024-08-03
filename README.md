# CodeShuttle

CodeShuttle is a command-line tool that streamlines code transfers between AI assistants and source files during pair programming sessions. It simplifies the process of applying AI-generated code changes to your project and provides a comprehensive change report.

## The Problem

When pair programming with an AI assistant:
1. The AI often generates code for multiple files simultaneously.
2. Manually copying and pasting this code into separate files is time-consuming and error-prone.
3. Keeping track of which code belongs to which file can be confusing.
4. There's no easy way to review all changes before applying them.

## The Solution

CodeShuttle solves these issues by:
1. Working with a standardized format for AI-generated code output.
2. Allowing you to apply multiple file changes with a single operation.
3. Providing an option to generate a comprehensive change report.

## How It Works

1. The AI assistant provides code in a specific format: a single text block with file paths and content clearly delimited.
2. You copy this entire block of text into a file or directly to CodeShuttle's input.
3. CodeShuttle parses the input, identifying individual files and their content.
4. It then creates or updates the specified files in your project, applying all changes at once.
5. Optionally, it generates a detailed report of all changes made.

This approach significantly reduces the time and effort needed to implement AI-suggested code changes across multiple files in your project.

## Installation

### Using Homebrew (macOS and Linux)

1. Tap the CodeShuttle repository:
   ```
   brew tap qlmmlp/tap
   ```

2. Install CodeShuttle:
   ```
   brew install codeshuttle
   ```

### Manual Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/codeshuttle.git
   cd codeshuttle
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Unix or MacOS
   .venv\Scripts\activate  # On Windows
   ```

3. Install the package in editable mode:
   ```
   pip install -e .
   ```

## Usage

To use CodeShuttle, run the following command:

```
codeshuttle --input <input_file> --root <output_directory> [--verbose] [--output <output_file>]
```

- `<input_file>`: Path to the input file containing the changes. Use `-` for stdin.
- `<output_directory>`: Root directory where changes will be applied.
- `--verbose`: (Optional) Enable verbose output.
- `--output <output_file>`: (Optional) Specify a file to write a comprehensive change report.

### Input File Format

The input file should follow this format:

```
### FILE_PATH: path/to/file1.ext
Content for file1

### FILE_PATH: path/to/file2.ext
Content for file2
```

### Example

1. Create an input file named `sample_changes.txt`:

```
### FILE_PATH: hello.py
print("Hello, World!")

### FILE_PATH: greetings/welcome.py
def welcome(name):
    return f"Welcome, {name}!"

print(welcome("CodeShuttle User"))

### FILE_PATH: config.json
{
  "version": "1.0",
  "environment": "development"
}
```

2. Run CodeShuttle:

```
codeshuttle --input sample_changes.txt --root ./output --verbose --output changes_report.txt
```

This will create or modify the specified files in the `./output` directory and generate a comprehensive change report in `changes_report.txt`.

## Change Report

When you specify an output file using the `--output` option, CodeShuttle generates a detailed report of all changes made. This report includes:

- The path of each file that was modified or created
- The entire content of each changed file

This feature is particularly useful for:
- Reviewing all changes before committing them to version control
- Keeping a record of AI-suggested modifications
- Sharing changes with team members for code review

## Development

### Running Tests

To run the tests, use the following command:

```
pytest
```

For more detailed output, use:

```
pytest -v
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.