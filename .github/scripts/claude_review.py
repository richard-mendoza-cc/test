import os
import sys
import requests

diff_file = sys.argv[1]
context_file = sys.argv[2]
pr_title = sys.argv[3]
pr_body = sys.argv[4]
pr_number = sys.argv[5]

with open(diff_file, 'r') as f:
    diff = f.read()
with open(context_file, 'r') as f:
    context = f.read()

prompt = f"""
You are a senior software engineer reviewing a GitHub pull request.
Review the following PR for:
- Bugs and logic errors
- Code style and best practices
- Documentation and comments
- Security concerns and edge cases
- Adequate test coverage

If you need more context from surrounding code, mention it in your review.

PR Title: {pr_title}
PR Description: {pr_body}
PR Diff:
{diff}
Changed File Content:
{context}
"""

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={"x-api-key": os.environ["CLAUDE_API_KEY"]},
    json={
        "model": "claude-3-opus-20240229",
        "max_tokens": 1200,
        "messages": [{"role": "user", "content": prompt}]
    }
)
review = response.json().get("content", "")

repo = os.environ.get("GITHUB_REPOSITORY")
github_token = os.environ["GITHUB_TOKEN"]
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
    headers={"Authorization": f"token {github_token}"},
    json={"body": review}
)
