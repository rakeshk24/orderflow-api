import time

from opentelemetry import trace
from opentelemetry.propagate import extract, inject
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from shared.metrics import errors_total, request_latency, requests_total


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ctx = extract(request.headers)

        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(
            f"{request.method} {request.url.path}",
            context=ctx,
        ) as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.target", request.url.path)

            start = time.time()
            response = await call_next(request)
            elapsed_ms = (time.time() - start) * 1000

            span.set_attribute("http.status_code", response.status_code)

            labels = {"http.method": request.method}
            request_latency.set(elapsed_ms, labels)
            requests_total.add(1, labels)
            if response.status_code >= 500:
                errors_total.add(1, labels)

            sc = span.get_span_context()
            response.headers["X-Trace-Id"] = format(sc.trace_id, "032x")

            return response
