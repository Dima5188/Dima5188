#!/usr/bin/env python
import sys
import re

# Define ANSI escape sequences for colored terminal output
RED = '\033[91m'  # Red text
GREEN = '\033[92m'  # Green text
BOLD = '\033[1m'  # Bold text
END = '\033[0m'  # Reset to default text formatting


def run_checks(file_list):
    """Read files and perform all checks."""
    try:
        with open(file_list, 'r') as file:
            files = file.read().splitlines()
    except FileNotFoundError:
        print(f"{RED}ERROR: File list '{file_list}' not found.{END}")
        sys.exit(1)

    all_errors = []

    for file in files:
        print(f"Checking file: {file}")
        if file.endswith('.lkml') and not file.endswith('_DEV.lkml'):
            # Call here for all the necessary checks:
            all_errors.extend(check_access_filter(file))

    if all_errors:
        print("\n".join(all_errors))
        sys.exit(1)  # Exit if there are errors
    else:
        print(f"{GREEN}All checks passed successfully.{END}")


def check_access_filter(file):
    """Check if each explore block has the required access_filter with user_attribute."""
    required_attributes = ['merchant_id']  # Add any other required attributes here
    errors = []
    try:
        with open(file, 'r') as f:
            content = f.read()

        # Extract all 'explore' blocks from the LookML file as a dictionary
        explore_pattern = r'explore:\s*(\w+)\s*{((?:[^{}]*|{[^{}]*})*)}'
        explores = dict(re.findall(explore_pattern, content, re.MULTILINE | re.DOTALL))

        if not explores:
            return [f"{RED}Error: No 'explore' blocks found in file. [{file}]{END}\n"]

        for explore_name, explore_content in explores.items():
            # Extract 'field' and 'user_attribute' pairs from access_filter blocks, handling multiline definitions
            access_filter_pattern = r'access_filter:\s*{\s*field:\s*(\S+)\s*user_attribute:\s*(\S+)\s*}'
            access_filters = [{'field': f, 'user_attribute': u} for f, u in re.findall(access_filter_pattern, explore_content, re.DOTALL)]

            if not access_filters:
                errors.append(f"{RED}Error: Missing access_filter in explore '{explore_name}'. [{file}]{END}")
                continue

            # Check if required user attributes are in access filters
            missing_attributes = [attr for attr in required_attributes if not any(af['user_attribute'] == attr for af in access_filters)]
            if missing_attributes:
                quoted_attrs = ', '.join(f"'{attr}'" for attr in missing_attributes)
                errors.append(f"{RED}Error: Missing required user attribute(s) {quoted_attrs} in explore '{explore_name}'. [{file}]{END}")
    except FileNotFoundError:
        errors.append(f"{RED}Error: File '{file}' does not exist.{END}")

    return errors


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{RED}ERROR: Usage: {sys.argv[0]} <file_list> <commit_message>{END}")
        sys.exit(1)

    file_list_path = sys.argv[1]
    run_checks(file_list_path)
