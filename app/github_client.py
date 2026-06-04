import hmac
import hashlib
import requests
from typing import Optional
from app.config import Config


class GitHubClient:
    """Thin wrapper around the GitHub REST API."""

    BASE = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or Config.GITHUB_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    # ------------------------------------------------------------------
    # Signature verification
    # ------------------------------------------------------------------

    @staticmethod
    def verify_signature(payload_bytes: bytes, signature: str, secret: str) -> bool:
        """Return True if the HMAC-SHA256 signature matches."""
        expected = "sha256=" + hmac.new(
            secret.encode(), payload_bytes, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    # ------------------------------------------------------------------
    # Pull Request helpers
    # ------------------------------------------------------------------

    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> dict:
        url = f"{self.BASE}/repos/{owner}/{repo}/pulls/{pr_number}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_pull_request_files(self, owner: str, repo: str, pr_number: int) -> list[dict]:
        """Return list of changed files with patch diffs."""
        url = f"{self.BASE}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_file_content(self, owner: str, repo: str, path: str, ref: str) -> str:
        """Fetch raw file content at a specific git ref."""
        url = f"{self.BASE}/repos/{owner}/{repo}/contents/{path}"
        resp = self.session.get(url, params={"ref": ref})
        if resp.status_code == 404:
            return ""
        resp.raise_for_status()
        import base64
        return base64.b64decode(resp.json()["content"]).decode("utf-8", errors="replace")

    # ------------------------------------------------------------------
    # Posting review comments
    # ------------------------------------------------------------------

    def post_review(self, owner: str, repo: str, pr_number: int, body: str, event: str = "COMMENT") -> dict:
        """Post a top-level PR review."""
        url = f"{self.BASE}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        resp = self.session.post(url, json={"body": body, "event": event})
        resp.raise_for_status()
        return resp.json()

    def post_review_comment(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        commit_id: str,
        path: str,
        line: int,
        body: str,
    ) -> dict:
        """Post an inline review comment on a specific line."""
        url = f"{self.BASE}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
        resp = self.session.post(url, json={
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "line": line,
            "side": "RIGHT",
        })
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def build_diff_context(self, files: list[dict], max_lines: int = Config.MAX_DIFF_LINES) -> str:
        """Combine per-file patches into a single diff string."""
        parts = []
        total = 0
        for f in files:
            patch = f.get("patch", "")
            if not patch:
                continue
            header = f"### File: {f['filename']} ({f['status']})\n"
            chunk = header + patch + "\n"
            lines = chunk.count("\n")
            if total + lines > max_lines:
                parts.append(f"### File: {f['filename']} — diff truncated (too large)\n")
                break
            parts.append(chunk)
            total += lines
        return "\n".join(parts)
