from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor


def tracing():
    """Запуск трассировки в ArizePhoenix для LangChain компонентов"""
    tracer_provider = register(
      project_name="mvp2.0",
      endpoint="http://phoenix:6006/v1/traces"
    )

    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)