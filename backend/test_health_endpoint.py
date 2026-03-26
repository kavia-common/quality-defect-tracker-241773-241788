import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    """Create a Flask test client for the application."""
    flask_app.testing = True
    with flask_app.test_client() as test_client:
        yield test_client


def test_health_endpoint_root_returns_200_and_expected_payload(client):
    """Health endpoint should return 200 and the expected JSON payload."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.is_json is True
    assert response.get_json() == {"message": "Healthy"}
