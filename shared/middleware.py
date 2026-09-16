from opentelemetry import trace
from opentelemetry.propagate import extract, inject
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


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

            response = await call_next(request)

            span.set_attribute("http.status_code", response.status_code)

            # Return trace-id in response so callers can correlate their request
            sc = span.get_span_context()
            response.headers["X-Trace-Id"] = format(sc.trace_id, "032x")

            return response
