#!/usr/bin/env python
import sys
import re

# ANSI escape sequences for red text
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


def read_file_lines(file_list):
    """Read file paths from the given file list."""
    try:
        with open(file_list, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return None


def process_sql_file(file, process_func):
    """Helper function to process each SQL file with a given processing function."""
    try:
        with open(file, 'r') as f:
            content = f.read()
            return process_func(file, content)
    except FileNotFoundError:
        return [f"{RED}Error: File '{file}' does not exist in the current context.{RESET}"]


def check_configuration(file, content):
    """Check if any '.sql' file has mismatches between configuration and Jinja2 template variables."""
    errors = []

    # Extract config attributes from the config part if it exists
    config_pattern = r"(\w+)\s*=\s*'([^']+)'"
    config_dict = dict(re.findall(config_pattern, content))

    # Find Jinja2 template variables
    template_pattern = r'{{\s*([\w_]+)\s*}}'
    template_vars = re.findall(template_pattern, content)
    exclude_out_of_scope_vars = ['date_frame']

    # Create a new list with items not in remove_list
    template_vars = [item for item in template_vars if item not in exclude_out_of_scope_vars]

    # Check if every config variable is used in the template
    for key in config_dict.keys():
        if key not in template_vars:
            errors.append(f"{RED}Error: Configuration variable '{key}' is set but not used in the template. [{file}]{RESET}\n")

    # Check if every template variable is configured
    for var in template_vars:
        if var not in config_dict:
            errors.append(f"{RED}Error: Jinja2 template variable '{var}' is used but not configured. [{file}]{RESET}\n")

    return errors


def check_files_for_text(file, content, search_text):
    """Check if any '.sql' file contains the specified search text."""
    if search_text in content:
        return [f"{RED}Error: '{search_text}' found in {file}{RESET}\n"]
    return []


def run_all_checks(file_list):
    """Run all the defined checks."""
    files = read_file_lines(file_list)
    if files is None:
        print(f"{RED}ERROR: File list '{file_list}' not found.{RESET}")
        sys.exit(1)

    all_errors = []
    for file in files:
        if file.endswith('.sql'):
            all_errors.extend(process_sql_file(file, lambda f, c: check_files_for_text(f, c, 'NO_MERGE')))
            all_errors.extend(process_sql_file(file, lambda f, c: check_files_for_text(f, c, 'DEV_FILE')))
            all_errors.extend(process_sql_file(file, check_configuration))

    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(1)
    else:
        print("All checks passed successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    file_list_path = sys.argv[1]
    run_all_checks(file_list_path)
