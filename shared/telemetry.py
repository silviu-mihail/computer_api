import json
from datetime import datetime, UTC
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import (SpanExporter,
                                            SpanExportResult,
                                            BatchSpanProcessor)
from opentelemetry.instrumentation.flask import FlaskInstrumentor


class JSONFileSpanExporter(SpanExporter):
    def __init__(self,
                 file_path="traces.json",
                 service_name="default-service"):
        self.file_path = file_path
        self.service_name = service_name

    def export(self, spans) -> SpanExportResult:
        for span in spans:
            data = {
                "service": self.service_name,
                "name": span.name,
                "start_time": span.start_time,
                "end_time": span.end_time,
                "duration_ms": (span.end_time - span.start_time) / 1e6,
                "attributes": dict(span.attributes),
                "status": str(span.status.status_code),
                "trace_id": span.context.trace_id,
                "span_id": span.context.span_id,
                "parent_id": span.parent.span_id if span.parent else None,
                "timestamp": datetime.now(UTC).isoformat() + "Z"
            }

            with open(self.file_path, "a") as f:
                f.write(json.dumps(data) + "\n")

        return SpanExportResult.SUCCESS


def init_telemetry(app,
                   service_name="default-service",
                   trace_file="traces.json"):
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: service_name}))
    )
    exporter = JSONFileSpanExporter(file_path=trace_file,
                                    service_name=service_name)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(exporter)
    )
    FlaskInstrumentor().instrument_app(app)
    return trace.get_tracer(__name__)
