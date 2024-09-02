#!/usr/bin/env python
import sys

# ANSI escape sequences for red text
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def check_files_for_no_merge(file_list_path):
    # Read the list of changed files
    with open(file_list_path, 'r') as file:
        changed_files = file.read().splitlines()

    # Check each file
    found_no_merge = False
    for file in changed_files:
        if file.endswith('.sql'):
            print(f"{BOLD}File: {file}{RESET}")
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    if 'NO_MERGE' in content:
                        print(f"{RED}ERROR: 'NO_MERGE' found in {file}{RESET}\n")
                        found_no_merge = True
            except FileNotFoundError:
                print(f"File {file} does not exist in the current context.")

    # Exit with a non-zero status if 'NO_MERGE' was found
    if found_no_merge:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_sql_files.py <file_list_path>")
        sys.exit(1)

    file_list_path = sys.argv[1]
    check_files_for_no_merge(file_list_path)
