from prometheus_client import Counter

chat_requests_total = Counter(
    'chat_requests_total',
    'Total number of chat requests'
)