import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Hello, Flask!" in r.data

def test_items(client):
    r = client.get("/api/items")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
