"""
Unit tests for FineTuner and PRDataCollector.
Run with:  pytest tests/ -v
"""
import json
import pathlib
import pytest
from unittest.mock import MagicMock, patch, mock_open

from app.data_collector import ReviewExample, PRDataCollector
from app.fine_tuner import FineTuner
from app.model_registry import get_active_model, set_active_model, clear_fine_tuned_model


# ------------------------------------------------------------------
# ReviewExample
# ------------------------------------------------------------------

def make_example(**kwargs) -> ReviewExample:
    defaults = dict(
        pr_number=1,
        pr_title="Fix SQL injection",
        diff="+" * 200,
        review_body="Use parameterised queries instead of f-strings. " * 5,
        reviewer="alice",
    )
    defaults.update(kwargs)
    return ReviewExample(**defaults)


def test_review_example_usable():
    ex = make_example()
    assert ex.is_usable()


def test_review_example_too_short_diff():
    ex = make_example(diff="+short")
    assert not ex.is_usable()


def test_review_example_too_short_review():
    ex = make_example(review_body="ok")
    assert not ex.is_usable()


def test_review_example_bot_reviewer():
    ex = make_example(reviewer="dependabot[bot]")
    assert not ex.is_usable()


def test_review_example_generic_lgtm():
    ex = make_example(review_body="lgtm")
    assert not ex.is_usable()


# ------------------------------------------------------------------
# FineTuner — JSONL formatting
# ------------------------------------------------------------------

@pytest.fixture
def ft(tmp_path, monkeypatch):
    monkeypatch.setattr("app.fine_tuner.FINETUNE_DIR", tmp_path)
    monkeypatch.setattr("app.fine_tuner.TRAINING_FILE", tmp_path / "training.jsonl")
    monkeypatch.setattr("app.fine_tuner.VALIDATION_FILE", tmp_path / "validation.jsonl")
    monkeypatch.setattr("app.fine_tuner.MODEL_ID_FILE", tmp_path / "model_id.txt")
    with patch("app.fine_tuner.openai.OpenAI"):
        tuner = FineTuner(api_key="test-key")
    return tuner, tmp_path


def test_write_jsonl_valid_format(ft):
    tuner, tmp_path = ft
    examples = [make_example(pr_number=i) for i in range(3)]
    out = tmp_path / "out.jsonl"
    tuner.write_jsonl(examples, out)

    lines = out.read_text().strip().split("\n")
    assert len(lines) == 3
    for line in lines:
        record = json.loads(line)
        assert "messages" in record
        roles = [m["role"] for m in record["messages"]]
        assert roles == ["system", "user", "assistant"]


def test_to_chat_record_contains_diff():
    ex = make_example(pr_title="My PR", diff="+x = 1\n" * 50)
    record = FineTuner._to_chat_record(ex)
    user_content = record["messages"][1]["content"]
    assert "My PR" in user_content
    assert "+x = 1" in user_content


def test_to_chat_record_assistant_is_review():
    ex = make_example(review_body="Please use parameterised queries everywhere.")
    record = FineTuner._to_chat_record(ex)
    assert "parameterised" in record["messages"][2]["content"]


def test_to_chat_record_score_hint():
    ex = make_example(score=3)
    record = FineTuner._to_chat_record(ex)
    assert "3/10" in record["messages"][2]["content"]


def test_not_enough_examples_raises(ft):
    tuner, _ = ft
    with pytest.raises(ValueError, match="at least"):
        tuner.run_pipeline([make_example()])


# ------------------------------------------------------------------
# Model registry
# ------------------------------------------------------------------

def test_get_active_model_default(tmp_path, monkeypatch):
    monkeypatch.setattr("app.model_registry.MODEL_ID_FILE", tmp_path / "model_id.txt")
    result = get_active_model("gpt-4o-mini")
    assert result == "gpt-4o-mini"


def test_get_active_model_fine_tuned(tmp_path, monkeypatch):
    model_file = tmp_path / "model_id.txt"
    model_file.write_text("ft:gpt-4o-mini:org:my-model:abc123")
    monkeypatch.setattr("app.model_registry.MODEL_ID_FILE", model_file)
    result = get_active_model("gpt-4o-mini")
    assert result == "ft:gpt-4o-mini:org:my-model:abc123"


def test_set_and_clear_model(tmp_path, monkeypatch):
    model_file = tmp_path / "model_id.txt"
    monkeypatch.setattr("app.model_registry.MODEL_ID_FILE", model_file)
    set_active_model("ft:gpt-4o-mini:org:test:xyz")
    assert get_active_model("default") == "ft:gpt-4o-mini:org:test:xyz"
    clear_fine_tuned_model()
    assert get_active_model("default") == "default"


# ------------------------------------------------------------------
# PRDataCollector stats
# ------------------------------------------------------------------

def test_summarise_empty():
    result = PRDataCollector.summarise([])
    assert result["count"] == 0


def test_summarise_with_examples():
    examples = [make_example(score=8), make_example(score=3), make_example(score=None)]
    result = PRDataCollector.summarise(examples)
    assert result["count"] == 3
    assert "8" in result["by_score"]
    assert "3" in result["by_score"]
