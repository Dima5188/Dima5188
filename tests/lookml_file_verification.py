#!/usr/bin/env python
import sys
import re

# Define ANSI escape sequences for colored terminal output
RED = '\033[91m'  # Red text
GREEN = '\033[92m'  # Green text
END = '\033[0m'  # Reset to default text formatting


def run_checks(file_list, bypass):
    """Read files and perform all checks."""
    try:
        with open(file_list, 'r') as file:
            files = file.read().splitlines()
    except FileNotFoundError:
        print(f"{RED}ERROR: File list '{file_list}' not found.{END}")
        sys.exit(1)

    if bypass:
        print(f"{GREEN}Bypassing all checks as per the commit message.{END}")
        return

    all_errors = []
    required_attributes = ['merchant_id', 'dima']  # Add any other required attributes here
    for file in files:
        if file.endswith('.lkml'):
            all_errors.extend(check_access_filter(file, required_attributes))

    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(1)  # Exit if there are errors
    else:
        print(f"{GREEN}All checks passed successfully.{END}")


def check_access_filter(file, required_attributes):
    """Check for 'access_filter' presence and specified user attributes."""
    errors = []
    try:
        with open(file, 'r') as f:
            content = f.read()
            pattern = r'^\s*access_filter:\s*{field:\s*(.*?)(?:\n\s*user_attribute:\s*(.*?))?\s*}'
            matches = re.findall(pattern, content, re.MULTILINE)

            if not matches:
                errors.append(f"{RED}Error: Required user attributes {', '.join(required_attributes)} are missing in LookML models. [{file}]{END}")
            else:
                access_filters = [{'field': match[0], 'user_attribute': match[1] or None} for match in matches]

                # Check for all required user attributes
                missing_attributes = [attr for attr in required_attributes if not any(access_filter.get('user_attribute') == attr for access_filter in access_filters)]
                if missing_attributes:
                    errors.append(f"{RED}Error: Required user attributes {', '.join(missing_attributes)} are missing in LookML models. [{file}]{END}")
    except FileNotFoundError:
        errors.append(f"{RED}Error: File '{file}' does not exist.{END}")

    return errors


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"{RED}ERROR: Usage: {sys.argv[0]} <file_list> <commit_message>{END}")
        sys.exit(1)

    file_list_path = sys.argv[1]
    commit_message = sys.argv[2]
    bypass_checks = '--bypass-checks' in commit_message

    run_checks(file_list_path, bypass_checks)
