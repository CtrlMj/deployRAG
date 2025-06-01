from app.main import load_prompt
import pytest

def test_prompt_template_contains_variables():
    prompt = load_prompt()
    variables = prompt.input_variables
    assert "context" in variables
    assert "question" in variables