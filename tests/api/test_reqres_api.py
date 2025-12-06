import requests
import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture
def api_base_url():
    """
    Fixture que devuelve la URL base de JSONPlaceholder.
    Mucho más estable que ReqRes para pruebas automatizadas.
    """
    return "https://jsonplaceholder.typicode.com"
def test_get_post(api_base_url):
    """GET /posts/1 -> 200 y campos esperados."""
    url = f"{api_base_url}/posts/1"
    response = requests.get(url)

    logger.info(f"GET {url} -> {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["id"] == 1
    assert "title" in data
def test_create_post(api_base_url):
    """POST /posts -> 201 + retorna datos enviados."""
    url = f"{api_base_url}/posts"
    payload = {"title": "Juan Tester", "body": "Mi post", "userId": 1}

    response = requests.post(url, json=payload)
    logger.info(f"POST {url} -> {response.status_code}")

    assert response.status_code == 201
    data = response.json()

    # JSONPlaceholder hace echo de los datos enviados
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
def test_delete_post(api_base_url):
    """DELETE /posts/1 -> 200 y respuesta vacía o {}."""
    url = f"{api_base_url}/posts/1"
    response = requests.delete(url)

    logger.info(f"DELETE {url} -> {response.status_code}")
    assert response.status_code == 200

    # Puede devolver {} o cadena vacía
    text = response.text.strip()
    assert text in ("", "{}", "{}\n")
