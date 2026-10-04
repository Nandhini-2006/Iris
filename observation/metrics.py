from prometheus_client import Counter, Histogram


DEBUG_REQUESTS = Counter(
    "debug_requests_total",
    "Total number of debug requests"
)

DEBUG_FAILURES = Counter(
    "debug_failures_total",
    "Total number of failed debug requests"
)

DEBUG_DURATION = Histogram(
    "debug_request_duration_seconds",
    "Time taken to process debug requests"
)