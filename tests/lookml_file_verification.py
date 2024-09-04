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
    for file in files:
        if file.endswith('.lkml'):
            all_errors.extend(check_access_filter(file))

    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(1)  # Exit if there are errors
    else:
        print("All checks passed successfully.")


def check_access_filter(file):
    """Check for 'access_filter' presence and 'merchant_id' user_attribute."""
    errors = []
    try:
        with open(file, 'r') as f:
            content = f.read()
            pattern = r'^\s*access_filter:\s*{field:\s*(.*?)(?:\n\s*user_attribute:\s*(.*?))?\s*}'
            matches = re.findall(pattern, content, re.MULTILINE)

            if not matches:
                errors.append(f"{RED}Error: No 'access_filter' found in [{file}].{END}")
            else:
                access_filters = []
                for match in matches:
                    access_filter = {
                        'field': match[0],  # Capture the field value
                        'user_attribute': match[1] if match[1] else None  # Capture the user_attribute value if present
                    }
                    access_filters.append(access_filter)

                if not any(access_filter_item.get('user_attribute') == 'merchant_id' for access_filter_item in access_filters):
                    errors.append(f"{RED}Error: 'merchant_id' not found in user_attribute in [{file}].{END}")
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
