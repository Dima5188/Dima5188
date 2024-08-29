import os
import subprocess


def get_changed_files():
    # Get the PR number from the environment variable
    pr_number = os.getenv('GITHUB_REF').split('/')[-1]
    # Use gh CLI to get the list of changed files in the PR
    result = subprocess.run(
        ['gh', 'pr', 'view', pr_number, '--json', 'files', '--jq', '.files[].path'],
        capture_output=True, text=True
    )
    return result.stdout.splitlines()


def check_files_for_no_merge(files):
    problematic_files = []
    for file in files:
        if file.endswith('.sql'):
            try:
                with open(file, 'r') as f:
                    if 'NO_MERGE' in f.read():
                        problematic_files.append(file)
            except FileNotFoundError:
                print(f"File {file} not found.")
    return problematic_files


def main():
    files = get_changed_files()
    problematic_files = check_files_for_no_merge(files)

    # Write problematic files to a temp file
    if problematic_files:
        with open('/tmp/problematic_files.txt', 'w') as f:
            f.write('\n'.join(problematic_files))
        exit(1)  # Fail the action if there are issues
    else:
        print("No issues found.")


if __name__ == "__main__":
    main()
