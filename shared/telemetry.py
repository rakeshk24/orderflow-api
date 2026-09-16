import os
import logging

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

logger = logging.getLogger(__name__)


def setup_telemetry(service_name: str) -> None:
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: os.getenv("SERVICE_VERSION", "0.1.0"),
        "deployment.environment": os.getenv("DEPLOYMENT_ENV", "development"),
    })

    provider = TracerProvider(resource=resource)

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
    try:
        exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        provider.add_span_processor(BatchSpanProcessor(exporter))
    except Exception:
        logger.warning("OTLP exporter unavailable — traces will not be exported")

    trace.set_tracer_provider(provider)
    logger.info("Telemetry initialised", extra={"service": service_name, "otel_endpoint": endpoint})
