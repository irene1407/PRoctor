"""
Collect historical PR review data from GitHub for fine-tuning.

Usage:
    from app.data_collector import PRDataCollector
    collector = PRDataCollector()
    examples = collector.collect(owner='pallets', repo='flask', max_prs=50)
"""

import time
import logging
from dataclasses import dataclass, field
from app.github_client import GitHubClient
from app.config import Config

logger = logging.getLogger(__name__)


@dataclass
class ReviewExample:
    """One training example: a diff paired with a human review comment."""
    pr_number: int
    pr_title: str
    diff: str
    review_body: str
    reviewer: str
    score: int | None = None
    metadata: dict = field(default_factory=dict)

    def is_usable(self, min_diff_chars: int = 100, min_review_chars: int = 80) -> bool:
        """Filter out trivially short or bot-generated examples."""
        if len(self.diff.strip()) < min_diff_chars:
            return False
        if len(self.review_body.strip()) < min_review_chars:
            return False
        bot_names = ("dependabot", "renovate", "github-actions", "codecov")
        if any(bot in self.reviewer.lower() for bot in bot_names):
            return False
        generic_phrases = ("lgtm", "looks good", "approved", "thank you", "thanks!")
        body_lower = self.review_body.lower().strip()
        if any(body_lower == g for g in generic_phrases):
            return False
        return True


class PRDataCollector:
    """Fetch closed, reviewed PRs and build a list of ReviewExample objects."""

    def __init__(self, token: str | None = None):
        self.gh = GitHubClient(token)

    def collect(
        self,
        owner: str,
        repo: str,
        max_prs: int = 100,
        state: str = "closed",
        rate_limit_sleep: float = 0.5,
    ) -> list[ReviewExample]:
        """
        Collect training examples from a repository.

        Args:
            owner:             GitHub org or username
            repo:              Repository name
            max_prs:           Max number of PRs to inspect
            state:             'closed' (default) or 'all'
            rate_limit_sleep:  Seconds to pause between API calls

        Returns:
            List of ReviewExample objects that pass the quality filter
        """
        logger.info(f"Collecting PRs from {owner}/{repo} (max {max_prs})")
        examples: list[ReviewExample] = []
        page = 1

        while len(examples) < max_prs:
            prs = self._fetch_pr_page(owner, repo, state, page)
            if not prs:
                break

            for pr in prs:
                if len(examples) >= max_prs:
                    break
                pr_number = pr["number"]
                try:
                    batch = self._process_pr(owner, repo, pr, rate_limit_sleep)
                    examples.extend(batch)
                    logger.info(f"  PR #{pr_number} → {len(batch)} usable example(s)")
                except Exception as exc:
                    logger.warning(f"  PR #{pr_number} skipped: {exc}")
                time.sleep(rate_limit_sleep)

            page += 1

        logger.info(f"Collection complete: {len(examples)} usable examples from {owner}/{repo}")
        return examples

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fetch_pr_page(self, owner: str, repo: str, state: str, page: int) -> list[dict]:
        url = f"{self.gh.BASE}/repos/{owner}/{repo}/pulls"
        resp = self.gh.session.get(url, params={"state": state, "per_page": 30, "page": page})
        resp.raise_for_status()
        return resp.json()

    def _fetch_pr_reviews(self, owner: str, repo: str, pr_number: int) -> list[dict]:
        url = f"{self.gh.BASE}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        resp = self.gh.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def _process_pr(
        self,
        owner: str,
        repo: str,
        pr: dict,
        sleep: float,
    ) -> list[ReviewExample]:
        pr_number = pr["number"]
        files = self.gh.get_pull_request_files(owner, repo, pr_number)
        diff = self.gh.build_diff_context(files)
        time.sleep(sleep)

        reviews = self._fetch_pr_reviews(owner, repo, pr_number)

        examples = []
        for review in reviews:
            body = (review.get("body") or "").strip()
            reviewer = review.get("user", {}).get("login", "")

            # Map GitHub review state to a numeric score hint
            state_score = {
                "APPROVED": 8,
                "CHANGES_REQUESTED": 3,
                "COMMENTED": None,
                "DISMISSED": None,
            }
            score = state_score.get(review.get("state", ""), None)

            example = ReviewExample(
                pr_number=pr_number,
                pr_title=pr.get("title", ""),
                diff=diff,
                review_body=body,
                reviewer=reviewer,
                score=score,
                metadata={
                    "repo": f"{owner}/{repo}",
                    "review_state": review.get("state"),
                    "submitted_at": review.get("submitted_at"),
                },
            )
            if example.is_usable():
                examples.append(example)

        return examples

    # ------------------------------------------------------------------
    # Stats helper
    # ------------------------------------------------------------------

    @staticmethod
    def summarise(examples: list[ReviewExample]) -> dict:
        if not examples:
            return {"count": 0}
        avg_diff = sum(len(e.diff) for e in examples) / len(examples)
        avg_review = sum(len(e.review_body) for e in examples) / len(examples)
        by_score = {}
        for e in examples:
            k = e.score if e.score is not None else "unknown"
            by_score[str(k)] = by_score.get(str(k), 0) + 1
        return {
            "count": len(examples),
            "avg_diff_chars": int(avg_diff),
            "avg_review_chars": int(avg_review),
            "by_score": by_score,
        }
