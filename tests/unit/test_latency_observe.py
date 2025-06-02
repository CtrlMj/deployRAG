import pytest
from prometheus_client import CollectorRegistry
from prometheus_client.metrics import Histogram
import time


@pytest.fixture
def latency_histogram():
    registry = CollectorRegistry()
    return Histogram(
        "chat_request_latency_seconds",
        "Chatbot request latency in seconds",
        registry=registry,
    )


def test_latency_histogram_observe(latency_histogram):
    start_time = time.time()
    time.sleep(0.1)
    latency = time.time() - start_time
    latency_histogram.observe(latency)

    samples = list(latency_histogram.collect())[0].samples
    assert any(
        sample.name == "chat_request_latency_seconds_bucket" for sample in samples
    )
