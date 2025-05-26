from prometheus_client import Counter, Histogram

# number of requests
chat_requests_total = Counter(
    'chat_requests_total',
    'Total number of chat requests'
)

# Latency
chat_request_latency_seconds = Histogram(
    'chat_request_latency_seconds',
    'Time taken to process a chat request in seconds'
)

# tokens per request (input + output)
chat_request_tokens = Histogram(
    'chat_request_tokens',
    'Number of tokens per chat request'
)