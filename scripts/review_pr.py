"""
GitHub Actions script — reviews a PR and posts the result as a comment.

Called by .github/workflows/pr_review_bot.yml
Environment variables are injected by the workflow.
"""

import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    owner    = os.environ["REPO_OWNER"]
    repo     = os.environ["REPO_NAME"]
    pr_num   = int(os.environ["PR_NUMBER"])
    pr_title = os.environ.get("PR_TITLE", "")
    pr_body  = os.environ.get("PR_BODY", "")

    logger.info(f"Reviewing PR #{pr_num} in {owner}/{repo}")

    from app.github_client import GitHubClient
    from app.ai_reviewer import AIReviewer

    gh = GitHubClient()
    reviewer = AIReviewer()

    files = gh.get_pull_request_files(owner, repo, pr_num)
    diff  = gh.build_diff_context(files)

    logger.info(f"Diff size: {len(diff)} characters across {len(files)} file(s)")

    review = reviewer.review_diff(diff=diff, pr_title=pr_title, pr_description=pr_body)
    comment = AIReviewer.format_as_markdown(review)

    gh.post_review(owner, repo, pr_num, comment)

    logger.info(f"Review posted — score {review.get('score')}/10, "
                f"{len(review.get('issues', []))} issue(s)")


if __name__ == "__main__":
    main()
