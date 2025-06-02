import requests
import requests
from main import create_rag_chain
from langchain_core.runnables import RunnablePassthrough


def test_metrics_endpoint_reachable():
    response = requests.get("http://localhost:8502/metrics")
    assert response.status_code == 200
    assert "chat_requests_total" in response.text


# def test_chat_request_increments_metric():

#     chain = create_rag_chain()

#     chain.invoke("What is the capital of France?")

#     response = requests.get("http://localhost:8502/metrics")
#     metrics_text = response.text

#     # Parse and assert metric is non-zero
#     for line in metrics_text.splitlines():
#         if line.startswith("chat_requests_total"):
#             value = float(line.split(" ")[-1])
#             assert value >= 1
#             break
#     else:
#         raise AssertionError("chat_requests_total not found in metrics")
