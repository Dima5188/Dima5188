#!/usr/bin/env python
import sys
import re

# ANSI escape sequences for red text
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


def check_configuration(file_list):
    """Check if any '.sql' file contains the specified search text."""
    try:
        with open(file_list, 'r') as file:
            changed_files = file.read().splitlines()
    except FileNotFoundError:
        return f"{RED}ERROR: File list '{file_list}' not found.{RESET}"

    errors = []
    for file in changed_files:
        if file.endswith('.sql'):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    # Extract config attributes from the config part if it exists
                    config_pattern = r"(\w+)\s*=\s*'([^']+)'"
                    config_dict = dict(re.findall(config_pattern, content))

                    # Find Jinja2 template variables
                    template_pattern = r'{{\s*([\w_]+)\s*}}'
                    template_vars = re.findall(template_pattern, content)

                    # Check if every config variable is used in the template
                    for key in config_dict.keys():
                        if key not in template_vars:
                            errors.append(f"{RED}Error: Configuration variable '{key}' is set but not used in the template. "
                                          f"[{file}]{RESET}\n")

                    # Check if every template variable is configured
                    for var in template_vars:
                        if var not in config_dict:
                            errors.append(f"{RED}Error: Jinja2 template variable '{var}' is used but not configured. "
                                          f"[{file}]{RESET}\n")

            except FileNotFoundError:
                errors.append(f"{RED}Error: File '{file}' does not exist in the current context.{RESET}")
    return errors if errors else "Success"


def check_files_for_text(file_list, search_text):
    """Check if any '.sql' file contains the specified search text."""
    try:
        with open(file_list, 'r') as file:
            changed_files = file.read().splitlines()
    except FileNotFoundError:
        return f"{RED}ERROR: File list '{file_list}' not found.{RESET}"

    errors = []
    for file in changed_files:
        if file.endswith('.sql'):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    if search_text in content:
                        errors.append(f"{RED}Error: '{search_text}' found in {file}{RESET}\n")
            except FileNotFoundError:
                errors.append(f"{RED}Error: File '{file}' does not exist in the current context.{RESET}")
    return errors if errors else "Success"


def run_all_checks(file_list):
    """Run all the defined checks."""
    checks = [
        lambda fl: check_files_for_text(fl, 'NO_MERGE'),
        lambda fl: check_files_for_text(fl, 'DEV_FILE'),
        lambda fl: check_configuration(fl),
    ]

    all_errors = []
    for check in checks:
        result = check(file_list)
        if result != "Success":
            if isinstance(result, list):
                all_errors.extend(result)
            else:
                all_errors.append(result)

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
