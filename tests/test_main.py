from fastapi.testclient import TestClient

from termci_api.app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello TermCI!'}