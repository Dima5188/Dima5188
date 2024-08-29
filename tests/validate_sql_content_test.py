#!/usr/bin/env python
import sys


def check_files_for_no_merge(file_list_path):
    # Read the list of changed files
    with open(file_list_path, 'r') as file:
        changed_files = file.read().splitlines()

    # Check each file
    found_no_merge = False
    for file in changed_files:
        if file.endswith('.sql'):
            print(f"Checking file: {file}")
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    if 'NO_MERGE' in content:
                        print(f"ERROR: 'NO_MERGE' found in {file}")
                        found_no_merge = True
            except FileNotFoundError:
                print(f"File {file} does not exist in the current context.")

    # Fail the job if 'NO_MERGE' was found in any SQL file
    if found_no_merge:
        raise Exception("One or more SQL files contain the 'NO_MERGE' string.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_sql_files.py <file_list_path>")
        sys.exit(1)

    file_list_path = sys.argv[1]
    check_files_for_no_merge(file_list_path)

