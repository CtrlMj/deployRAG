import pytest
from unittest.mock import patch, MagicMock
from main import load_knowledgeBase

def test_call_knowledgeBase():
    with patch("main.OpenAIEmbeddings") as mock_embed_class, \
         patch("main.FAISS.load_local") as mock_faiss_load_local:
        
        mock_embed_instance = MagicMock()
        mock_embed_class.return_value = mock_embed_instance
        
        mock_faiss_instance = MagicMock()
        mock_faiss_load_local.return_value = mock_faiss_instance

        kb = load_knowledgeBase(db_faiss_path="app/vectorstore/db_faiss")

        assert kb == mock_faiss_instance

        mock_faiss_load_local.assert_called_once_with(
            "app/vectorstore/db_faiss",
            mock_embed_instance,
            allow_dangerous_deserialization=True
        )
