import time

from opentelemetry import metrics

# No MeterProvider has been configured — metrics.get_meter() returns a no-op meter.
# Every instrument created here silently discards all recorded values;
# nothing is exported to Dynatrace/Datadog. The app runs without errors,
# making this invisible without explicitly verifying the exporter pipeline.
meter = metrics.get_meter("orderflow")

# Gauge records only the most recent value — there is no history.
# Dynatrace cannot compute p50/p95/p99 latency percentiles from a Gauge.
# The correct instrument is a Histogram (http.server.request.duration).
request_latency = meter.create_gauge(
    "request_latency",
    description="HTTP request latency",
    unit="ms",
)

# Non-standard names — OTel semantic conventions define:
#   http.server.request.duration  (Histogram)
#   http.server.active_requests   (UpDownCounter)
# Custom names like these are invisible to Dynatrace's built-in HTTP dashboards.
requests_total = meter.create_counter(
    "requests_total",
    description="Total number of HTTP requests received",
)

errors_total = meter.create_counter(
    "errors",
    description="Total number of errors",
)

# Business metrics — correct intent but also silently dropped
# because the MeterProvider is not configured.
orders_created = meter.create_counter(
    "orders_created",
    description="Number of orders successfully created",
)

payment_amount = meter.create_counter(
    "payment_amount",
    description="Total payment amount processed",
    unit="USD",
)
