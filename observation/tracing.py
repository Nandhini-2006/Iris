import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_tracing(app):

    service_name = os.getenv("OTEL_SERVICE_NAME", "ai-debugger-api")

    resource = Resource.create({
        "service.name": service_name
    })

    provider = TracerProvider(
        resource=resource
    )

    otlp_endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://localhost:4318"
    )

    exporter = OTLPSpanExporter(
        endpoint=f"{otlp_endpoint}/v1/traces"
    )

    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )

    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)