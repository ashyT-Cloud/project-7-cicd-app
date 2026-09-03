from app.main import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "project-7-cicd-app"
    assert data["version"] == "0.1.0"


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_version():
    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200

    data = response.get_json()

    assert data["application"] == "project-7-cicd-app"
    assert data["version"] == "0.1.0"
