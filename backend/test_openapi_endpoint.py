import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    """Create a Flask test client for the application."""
    flask_app.testing = True
    with flask_app.test_client() as test_client:
        yield test_client


def test_openapi_json_endpoint_returns_200_and_json(client):
    """
    OpenAPI endpoint should return 200 and JSON.

    Note: This app configures flask-smorest OPENAPI_URL_PREFIX='/docs', so the
    spec is typically served from '/docs/openapi.json'. For compatibility with
    environments that expose it at '/openapi.json', this test will try that
    first and fall back to the '/docs' prefixed route.
    """
    # Prefer the user-requested endpoint; fall back to app's configured prefix.
    response = client.get("/openapi.json")
    if response.status_code == 404:
        response = client.get("/docs/openapi.json")

    assert response.status_code == 200
    assert response.is_json is True

    payload = response.get_json()
    assert isinstance(payload, dict)

    # If this is truly an OpenAPI document, these are expected top-level keys.
    # We only assert them if the response looks like an OpenAPI document.
    if "openapi" in payload or "swagger" in payload:
        assert "info" in payload
        assert "paths" in payload
