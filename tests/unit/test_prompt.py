from app.main import load_prompt
import pytest

def test_prompt_template_contains_variables():
    prompt = load_prompt()
    template = prompt.template
    assert "{context}" in template
    assert "{question}" in template