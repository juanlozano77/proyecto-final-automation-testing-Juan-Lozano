import requests
from faker import Faker
from utils.logger import get_logger

logger = get_logger(__name__)
fake = Faker()


def test_create_post_with_faker():
    """
    Crear un post usando datos generados por Faker.
    Esperado:
    - Código 201
    - La respuesta debe contener los mismos campos enviados
    """

    base_url = "https://jsonplaceholder.typicode.com/posts"

    payload = {
        "title": fake.sentence(),
        "body": fake.paragraph(),
        "userId": fake.random_int(min=1, max=100)
    }

    logger.info(f"[FAKER API] Payload generado: {payload}")

    response = requests.post(base_url, json=payload)

    assert response.status_code == 201, (
        f"Esperado 201. Obtenido: {response.status_code}"
    )

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
