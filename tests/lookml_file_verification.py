#!/usr/bin/env python
import sys
import re

# Define ANSI escape sequences for colored terminal output
RED = '\033[91m'  # Red text
GREEN = '\033[92m'  # Green text
BOLD = '\033[1m'  # Bold text
END = '\033[0m'  # Reset to default text formatting


def read_file_lines(file_list):
    """Read lines from a file that contains a list of file paths.
    Args:
        file_list (str): The path to the file containing the list of file paths.
    Returns:
        list: A list of file paths.
        None: If the file is not found.
    """
    try:
        with open(file_list, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return None


def process_sql_file(file, process_func):
    """Process an SQL file using a provided function.
    Args:
        file (str): The path to the SQL file.
        process_func (function): A function that takes the file path and content
                                 and returns a list of errors or issues.

    Returns:
        list: A list of error messages or issues found in the file.
    """
    try:
        with open(file, 'r') as f:
            content = f.read()
            return process_func(file, content)
    except FileNotFoundError:
        return [f"{RED}Error: File '{file}' does not exist in the current context.{END}"]


def check_configuration(file, content):
    """Check for mismatches between configuration variables and Jinja2 template variables in an SQL file.
    Args:
        file (str): The path to the SQL file.
        content (str): The content of the SQL file.
    Returns:
        list: A list of error messages for any mismatches found.
    """
    errors = []

    # Use regex to find the desired part
    pattern = r'^\s*access_filter:\s*{field:\s*(.*?)(?:\n\s*user_attribute:\s*(.*?))?\s*}'

    matches = re.findall(pattern, content, re.MULTILINE)

    if matches:
        # Create a list to store the extracted information for each access_filter
        access_filters = []

        for match in matches:
            access_filter = {
                'field': match[0],  # Capture the field value
                'user_attribute': match[1] if match[1] else None  # Capture the user_attribute value if present
            }
            access_filters.append(access_filter)

        print(f"access_filters: {access_filters}")
    else:
        print("No match found.")

    return errors


def run_all_checks(file_list, bypass):
    """Run all the defined checks on the files listed in the file list.
    Args:
        file_list (str): The path to the file containing the list of file paths.
        bypass (bool): If True, bypass all checks.
    Returns:
        None: Exits the program if there are errors or if the file list is not found.
    """
    files = read_file_lines(file_list)

    if bypass:
        print(f"{GREEN}Bypassing all checks as per the commit message.{END}")
        return

    if files is None:
        print(f"{RED}ERROR: File list '{file_list}' not found.{END}")
        sys.exit(1)

    all_errors = []
    for file in files:
        if file.endswith('.lkml'):
            # Perform the configuration check on each SQL file
            all_errors.extend(process_sql_file(file, check_configuration))

    if all_errors:
        for error in all_errors:
            print(error)
        sys.exit(1)  # Exit with an error code if there are any errors
    else:
        print("All checks passed successfully.")  # Print success message if no errors are found


if __name__ == "__main__":
    # Ensure the correct number of arguments is provided
    if len(sys.argv) != 3:
        print(f"{RED}ERROR: Usage: {sys.argv[0]} <file_list> <commit_message>{END}")
        sys.exit(1)

    # Assign command-line arguments to variables
    file_list_path = sys.argv[1]
    commit_message = sys.argv[2]

    # Check for the bypass flag in the commit message
    bypass_checks = '--bypass-checks' in commit_message

    # Run the checks on the files listed in the file list
    run_all_checks(file_list_path, bypass_checks)
