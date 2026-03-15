from google import genai
from google.genai import types
from app.config import settings


def get_genai_client() -> genai.Client:
    if settings.USE_VERTEX_AI:
        return genai.Client(
            vertexai=True,
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION,
            http_options=types.HttpOptions(api_version="v1"),
        )

    raise ValueError("This project is configured to use Vertex AI only.")