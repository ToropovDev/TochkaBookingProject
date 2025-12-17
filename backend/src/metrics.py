from prometheus_client import Counter, Gauge

REQUESTS_TOTAL = Counter(
    "fastapi_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUESTS_ERRORS = Counter(
    "fastapi_http_requests_errors_total",
    "Total HTTP requests with 4xx or 5xx status",
    ["method", "endpoint", "status"],
)

REQUESTS_DURATION = Gauge(
    "fastapi_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

CPU_PERCENT = Gauge(
    "fastapi_process_cpu_percent", "CPU usage of the FastAPI process (%)"
)
MEMORY_RSS = Gauge(
    "fastapi_process_memory_rss_bytes",
    "RSS memory usage of the FastAPI process (bytes)",
)
MEMORY_PERCENT = Gauge(
    "fastapi_process_memory_percent", "Memory usage of the FastAPI process (%)"
)

EMAIL_SENT = Counter(
    "email_sent_total", "Total number of emails successfully sent", ["email_type"]
)

EMAIL_SEND_ERRORS = Counter(
    "email_send_errors_total",
    "Total number of failed email sending attempts",
    ["email_type"],
)
