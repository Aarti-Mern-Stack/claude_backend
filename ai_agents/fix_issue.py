import os
import glob

import anthropic
from github import Github


def get_latest_open_issue():
    """Read the latest open GitHub issue from the repository."""
    token = os.environ["GITHUB_TOKEN"]
    g = Github(token)

    repo_name = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo_name:
        raise RuntimeError("GITHUB_REPOSITORY environment variable is not set")

    repo = g.get_repo(repo_name)
    issues = repo.get_issues(state="open", sort="created", direction="desc")

    for issue in issues:
        if issue.pull_request is None:
            return issue

    raise RuntimeError("No open issues found")


def read_backend_code():
    """Read backend source files from routes/, controllers/, and models/."""
    code_files = {}
    patterns = ["routes/**/*.js", "controllers/**/*.js", "models/**/*.js"]

    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            with open(filepath, "r", encoding="utf-8") as f:
                code_files[filepath] = f.read()

    return code_files


def build_prompt(issue_title, issue_body, code_files):
    """Build the prompt for Claude with issue details and backend code."""
    code_section = ""
    for filepath, content in code_files.items():
        code_section += f"\n--- {filepath} ---\n{content}\n"

    return (
        f"You are a senior backend developer. A GitHub issue has been reported.\n\n"
        f"**Issue Title:** {issue_title}\n"
        f"**Issue Description:**\n{issue_body}\n\n"
        f"Below is the backend source code from this repository:\n"
        f"{code_section}\n\n"
        f"Analyze the code and the issue. Identify the root cause and suggest a fix. "
        f"Include the exact file name, the problematic code, and the corrected code."
    )


def ask_claude(prompt):
    """Send the prompt to Claude API and return the response."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def main():
    print("Fetching latest open issue...")
    issue = get_latest_open_issue()
    print(f"Issue #{issue.number}: {issue.title}")

    print("Reading backend code...")
    code_files = read_backend_code()
    print(f"Found {len(code_files)} source file(s)")

    print("Sending to Claude for analysis...")
    prompt = build_prompt(issue.title, issue.body or "", code_files)
    response = ask_claude(prompt)

    print("\n--- Claude's Analysis and Suggested Fix ---\n")
    print(response)


if __name__ == "__main__":
    main()
