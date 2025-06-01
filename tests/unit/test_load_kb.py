import pytest
from unittest.mock import patch, MagicMock
from app.main import load_knowledgeBase

def test_call_knowledgeBase():
    with patch("main.OpenAIEmbeddings") as mock_embed_class, \
         patch("main.FAISS") as mock_faiss_class:
        
        mock_embed_instance = MagicMock()
        mock_embed_class.return_value = mock_embed_instance
        
        mock_faiss_instance = MagicMock()
        mock_faiss_class.load_local.return_value = mock_faiss_instance

        kb = load_knowledgeBase()

        mock_faiss_class.load_local.assert_called_once_with(
            './vectorstore/db_faiss',
            mock_embed_instance,
            allow_dangerous_deserialization=True
        )

        assert kb == mock_faiss_instance
