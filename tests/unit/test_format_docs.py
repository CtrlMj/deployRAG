import pytest
from main import format_docs

class MockDocument:
    def __init__(self, content):
        self.page_content = content

def test_format_docs():
    docs = [MockDocument("Page 1"), MockDocument("Page 2"), MockDocument("Page 3")]
    result = format_docs(docs)
    assert result == "Page 1\n\nPage 2\n\nPage 3"
