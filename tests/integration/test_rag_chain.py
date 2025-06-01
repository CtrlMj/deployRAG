import pytest
from unittest.mock import patch, MagicMock
import app.main as main

@pytest.fixture
def mock_langchain_pipeline():
    with patch("main.load_knowledgeBase") as mock_load_kb, \
         patch("main.load_llm") as mock_load_llm, \
         patch("main.load_prompt") as mock_load_prompt, \
         patch("main.OpenAIEmbeddings") as mock_embeddings, \
         patch("main.FAISS") as mock_faiss, \
         patch("main.chat_requests_total") as mock_counter, \
         patch("main.chat_request_latency_seconds") as mock_latency, \
         patch("main.chat_request_tokens") as mock_token_metric:

        # Set up mocks
        mock_retriever = MagicMock()
        mock_faiss_instance = MagicMock()
        mock_faiss_instance.as_retriever.return_value = mock_retriever
        mock_load_kb.return_value = mock_faiss_instance

        mock_llm = MagicMock()
        mock_load_llm.return_value = mock_llm

        mock_prompt = MagicMock()
        mock_load_prompt.return_value = mock_prompt

        
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = MagicMock(
            content="Test response",
            usage_metadata={"total_tokens": 42}
        )

    
        with patch("main.RunnablePassthrough") as mock_passthrough:

            mock_passthrough.return_value = MagicMock()

            yield {
                "retriever": mock_retriever,
                "chain": mock_chain,
                "metrics": {
                    "counter": mock_counter,
                    "latency": mock_latency,
                    "tokens": mock_token_metric,
                }
            }



def test_process_query_invokes_chain_and_metrics(mock_langchain_pipeline):
    # Arrange
    query = "What is LangChain?"
    kb = main.load_knowledgeBase()
    prompt = main.load_prompt()
    llm = main.load_llm()

    # Act
    response = main.process_query(query, kb, prompt, llm)

    # Assert
    assert response == "Test response"
    mock_langchain_pipeline["metrics"]["counter"].inc.assert_called_once()
    mock_langchain_pipeline["metrics"]["latency"].observe.assert_called()
    mock_langchain_pipeline["metrics"]["tokens"].observe.assert_called_with(42)
