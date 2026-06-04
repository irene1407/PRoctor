"""
Scheduled retraining script — called by the weekly_retrain GitHub Actions workflow.

Environment variables required:
    OPENAI_API_KEY  — OpenAI secret key
    GITHUB_TOKEN    — GitHub personal access token (repo scope)
    TARGET_OWNER    — GitHub org or username to collect PRs from
    TARGET_REPO     — Repository name to collect PRs from
    MAX_PRS         — Max number of PRs to collect (default: 100)
    N_EPOCHS        — Fine-tuning epochs (default: 3)
"""

import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    owner    = os.environ.get("TARGET_OWNER")
    repo     = os.environ.get("TARGET_REPO")
    max_prs  = int(os.environ.get("MAX_PRS", 100))
    n_epochs = int(os.environ.get("N_EPOCHS", 3))

    if not owner or not repo:
        logger.error("TARGET_OWNER and TARGET_REPO must be set.")
        sys.exit(1)

    logger.info(f"Starting retrain: {owner}/{repo}, max_prs={max_prs}, epochs={n_epochs}")

    from app.data_collector import PRDataCollector
    from app.fine_tuner import FineTuner

    # 1. Collect
    collector = PRDataCollector()
    examples = collector.collect(owner=owner, repo=repo, max_prs=max_prs)
    stats = PRDataCollector.summarise(examples)
    logger.info(f"Collected {stats['count']} usable examples")

    if stats["count"] < 10:
        logger.warning(f"Only {stats['count']} examples — need at least 10. Skipping training.")
        sys.exit(0)

    # 2. Fine-tune
    tuner = FineTuner()
    result = tuner.run_pipeline(examples, n_epochs=n_epochs)

    logger.info("=" * 60)
    logger.info("Retraining complete!")
    logger.info(f"  Job ID           : {result['job_id']}")
    logger.info(f"  Fine-tuned model : {result['fine_tuned_model']}")
    logger.info(f"  Status           : {result['status']}")
    logger.info("=" * 60)

    if result["status"] != "succeeded":
        logger.error(f"Job did not succeed: {result['status']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
