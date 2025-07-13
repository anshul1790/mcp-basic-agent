# app/tools/github_tool.py
import requests
import json

def summarize_github_issue(url: str) -> str:
    try:
        # Parse GitHub issue URL
        parts = url.strip("/").split("/")
        if "github.com" not in url or len(parts) < 5:
            return "Invalid GitHub issue URL."

        owner, repo, _, issue_number = parts[-4:]

        issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "mcp-agent"
        }

        issue_res = requests.get(issue_url, headers=headers)
        issue_res.raise_for_status()
        issue_data = issue_res.json()

        comments_res = requests.get(comments_url, headers=headers)
        comments_res.raise_for_status()
        comments_data = comments_res.json()

        comment_texts = [c["body"][:200] for c in comments_data[:3]]  # First 3 comments

        summary_payload = {
            "title": issue_data.get("title"),
            "author": issue_data.get("user", {}).get("login"),
            "body": issue_data.get("body", "")[:500],
            "num_comments": len(comments_data),
            "top_comments": comment_texts
        }

        return json.dumps(summary_payload)

    except Exception as e:
        return f"Error: {str(e)}"

# ✅ Add the missing tool_schema so it can be imported
tool_schema = {
    "type": "function",
    "function": {
        "name": "summarize_github_issue",
        "description": "Summarizes a GitHub issue using its URL",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full GitHub issue URL (e.g. https://github.com/openai/openai-python/issues/2396)"
                }
            },
            "required": ["url"]
        }
    }
}
