import requests
import json
from uuid import uuid4

print("Running tests")

with open("mock.json") as f:
    mock_models = json.load(f)

short_response = mock_models["mock_model"]["short_response"]
long_response = mock_models["mock_model"]["long_response"]

url = "http://llm_router:8000"

def test_generate():
    uuid = str(uuid4())
    payload = {"uuid": uuid, "prompt": "test", "preprompt": "test", "model": "mock_model"}
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 200
    assert response.json()["generation"] == short_response

def test_generate_error():
    uuid = str(uuid4())
    payload = {"uuid": uuid, "prompt": "error", "preprompt": "test", "model": "mock_model"}
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 500
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 500

def test_generate_long():
    uuid = str(uuid4())
    payload = {"uuid": uuid, "prompt": "long_prompt", "preprompt": "test", "model": "mock_model"}
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 422
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 422

def test_generate_long_response():
    uuid = str(uuid4())
    payload = {"uuid": uuid, "prompt": "long_response", "preprompt": "test", "model": "mock_model"}
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 200
    assert response.json()["generation"] == long_response

def test_generate_model_not_found():
    uuid = str(uuid4())
    payload = {"uuid": uuid, "prompt": "test", "preprompt": "test", "model": "not_found"}
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 404
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 404

def test_generate_cache():
    uuid = str(uuid4())
    payload = {"uuid": uuid, "prompt": "test", "preprompt": "test", "model": "mock_model"}
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 200
    assert response.json()["generation"] == short_response
    response = requests.post(url + "/generate", json=payload)
    assert response.status_code == 200
    assert response.json()["generation"] == short_response

