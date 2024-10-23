import os
import json
import argparse
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description='Codebase Extractor Utility')
    parser.add_argument('-d', '--directory', type=str, default='.', help='Root directory to scan')
    parser.add_argument('-e', '--extensions', nargs='+', default=['.py', '.txt', '.md'], help='File extensions to include (e.g., .py .txt .md)')
    parser.add_argument('-x', '--exclude', nargs='+', default=['.git', '__pycache__', 'venv', 'node_modules'], help='Directories to exclude')
    parser.add_argument('-o', '--output', type=str, default='output', help='Output file prefix')
    parser.add_argument('-i', '--include-hidden', action='store_true', help='Include hidden files and directories (starting with a dot)')
    return parser.parse_args()

def is_plaintext_file(filename, include_extensions):
    _, ext = os.path.splitext(filename)
    return ext.lower() in include_extensions

def generate_tree_hierarchy(root_dir, exclude_dirs, include_hidden):
    tree_lines = []
    for root, dirs, files in os.walk(root_dir):
        # Exclude specified directories and hidden directories
        dirs[:] = [
            d for d in dirs
            if (include_hidden or not d.startswith('.')) and d not in exclude_dirs
        ]
        level = os.path.relpath(root, root_dir).count(os.sep)
        indent = '    ' * level
        subdir = os.path.basename(root)
        if level == 0:
            tree_lines.append(f'{subdir}/')
        else:
            tree_lines.append(f'{indent}{subdir}/')
        # Filter hidden files if include_hidden is False
        files = [f for f in files if include_hidden or not f.startswith('.')]
        for f in sorted(files):
            path = os.path.join(root, f)
            indent = '    ' * (level + 1)
            tree_lines.append(f'{indent}{f}')
    return tree_lines

def scan_directory(root_dir, include_extensions, exclude_dirs, include_hidden):
    file_contents = []
    for current_path, dirs, files in os.walk(root_dir):
        # Exclude specified directories and hidden directories
        dirs[:] = [
            d for d in dirs
            if (include_hidden or not d.startswith('.')) and d not in exclude_dirs
        ]
        # Filter hidden files if include_hidden is False
        files = [f for f in files if include_hidden or not f.startswith('.')]
        for file_name in files:
            full_path = os.path.join(current_path, file_name)
            rel_path = os.path.relpath(full_path, root_dir)
            if is_plaintext_file(file_name, include_extensions):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Get file metadata
                    stats = os.stat(full_path)
                    last_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
                    size = stats.st_size
                    file_contents.append({
                        'file_name': rel_path.replace('\\', '/'),
                        'file_text': content,
                        'last_modified': last_modified,
                        'size': size
                    })
                except Exception as e:
                    file_contents.append({
                        'file_name': rel_path.replace('\\', '/'),
                        'file_text': f'Error reading file: {e}',
                        'last_modified': None,
                        'size': None
                    })
    return file_contents

def main():
    args = parse_arguments()
    root_dir = os.path.abspath(args.directory)
    include_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]
    include_extensions = [ext.lower() for ext in include_extensions]
    exclude_dirs = set(args.exclude)
    include_hidden = args.include_hidden

    # Generate file hierarchy map
    tree_hierarchy = generate_tree_hierarchy(root_dir, exclude_dirs, include_hidden)

    # Scan directory and get file contents with metadata
    file_contents = scan_directory(root_dir, include_extensions, exclude_dirs, include_hidden)

    # Write the tree hierarchy to a text file
    hierarchy_file = f'{args.output}_hierarchy.txt'
    with open(hierarchy_file, 'w', encoding='utf-8') as f:
        for line in tree_hierarchy:
            f.write(line + '\n')

    # Write the file contents to a JSON file
    contents_file = f'{args.output}_contents.json'
    with open(contents_file, 'w', encoding='utf-8') as f:
        json.dump(file_contents, f, ensure_ascii=False, indent=2)

    print(f'File hierarchy written to {hierarchy_file}')
    print(f'File contents written to {contents_file}')

if __name__ == '__main__':
    main()
