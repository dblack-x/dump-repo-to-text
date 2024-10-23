# Codebase Extractor Utility

A Python script that extracts the file hierarchy and contents of plaintext files from a codebase. This utility is designed to help large language models (LLMs) read and understand codebases by providing a structured representation of the project.

## Features

- **Traverse Directories**: Recursively scans the specified root directory.
- **Include Specific File Types**: Only includes files with specified extensions (e.g., `.py`, `.txt`, `.md`).
- **Exclude Specific Directories**: Skips over directories like `.git`, `__pycache__`, `venv`, and `node_modules`.
- **Generate Tree-like Hierarchy Map**: Creates a visual representation of the directory structure.
- **Extract File Contents with Metadata**: Reads the contents of each file and includes metadata such as last modified time and file size.
- **Command-Line Interface (CLI)**: Customize the utility through command-line arguments.

## Requirements

- Python 3.x

## Installation

Clone this repository or download the script directly.

    git clone https://github.com/yourusername/codebase-extractor.git

## Usage

Navigate to the directory containing the script:

    cd dump-repo-to-text

Run the script with default settings:

    python codebase_extractor.py

### Command-Line Arguments

- `-d`, `--directory`: Root directory to scan (default: `.`)
- `-e`, `--extensions`: File extensions to include (default: `.py`, `.txt`, `.md`)
- `-x`, `--exclude`: Directories to exclude (default: `.git`, `__pycache__`, `venv`, `node_modules`)
- `-o`, `--output`: Output file prefix (default: `output`)

### Examples

#### Scan a Specific Directory

    python codebase_extractor.py -d /path/to/your/project

#### Include Additional File Types

    python codebase_extractor.py -e .py .txt .md .json

#### Exclude Additional Directories

    python codebase_extractor.py -x .git __pycache__ venv build dist

#### Specify Output File Names

    python codebase_extractor.py -o myproject

This will create `myproject_hierarchy.txt` and `myproject_contents.json`.

## Output Files

### Hierarchy File (`*_hierarchy.txt`)

Contains a tree-like representation of the directory structure.

**Example:**

    project/
        README.md
        setup.py
        src/
            main.py
            utils.py
        docs/
            index.md
        tests/
            test_main.py

### Contents File (`*_contents.json`)

A JSON file containing an array of file objects with the following fields:

- `file_name`: Relative path to the file from the root directory.
- `file_text`: The content of the file.
- `last_modified`: Last modified timestamp of the file.
- `size`: Size of the file in bytes.

**Example:**

    [
      {
        "file_name": "src/main.py",
        "file_text": "import os\n\n\ndef main():\n    print(\"Hello, World!\")\n",
        "last_modified": "2023-10-05 14:48:00",
        "size": 1024
      },
      {
        "file_name": "README.md",
        "file_text": "# Project Title\n\nA brief description of the project.\n",
        "last_modified": "2023-10-04 10:30:25",
        "size": 512
      }
    ]

## Notes

- **Encoding**: The script uses UTF-8 encoding for reading and writing files.
- **Error Handling**: If a file cannot be read, the `file_text` field will contain an error message, and `last_modified` and `size` will be `null`.
- **Cross-Platform Compatibility**: The script replaces backslashes with forward slashes in file paths for consistency across different operating systems.