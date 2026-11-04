from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_count_tokens():
    response = client.post("/count-tokens", json={"text": "Hello world"})

    assert response.status_code == 200
    assert response.json()["text"]=="Hello world"
    assert response.json()["token_count"] == 2


def test_empty_text():
    response = client.post("/count-tokens", json={"text": ""})

    assert response.status_code == 422

def test_missing_text():
    response = client.post("/count-tokens", json={})
    
    assert response.status_code == 422

def test_optimize_text():
    response = client.post(
        "/optimize",
        json={"text": "Python is useful.\nToken optimization saves money.\nPython is useful."}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["optimized_text"] == ("Python is useful.\nToken optimization saves money.")

    assert data["tokens_saved"] == (data["original_token_count"] - data["optimized_token_count"])

    assert data["savings_Percentage"] >=0


def test_optimize_empty_text():
    response = client.post(
        "/optimize",
        json={"text": ""}
    )

    assert response.status_code == 422