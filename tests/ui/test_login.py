import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data_loader import load_invalid_logins_from_csv
from utils.logger import get_logger

logger = get_logger(__name__)

INVALID_LOGIN_ROWS = load_invalid_logins_from_csv("resources/test_data/invalid_logins.csv")


@pytest.mark.parametrize("user_key", ["standard_user", "problem_user"])
def test_login_success(driver, base_url, valid_users, user_key):
    """Login exitoso con distintos usuarios válidos."""
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    user = valid_users[user_key]
    logger.info(f"[LOGIN OK] Usuario: {user['username']}")

    login_page.open_login_page(base_url)
    login_page.login(user["username"], user["password"])

    assert inventory_page.is_loaded(), "Esperado: ir al inventario. Obtenido: la página de inventario NO cargó."


@pytest.mark.parametrize(
    "row",
    INVALID_LOGIN_ROWS,
    ids=[r.get("id", f"case_{i}") for i, r in enumerate(INVALID_LOGIN_ROWS)]
)
def test_login_invalid_credentials(driver, base_url, row, request):
    """
    Escenarios negativos de login.
    Usa datos parametrizados desde CSV:
    - escenario
    - credenciales inválidas
    - mensaje de error esperado
    """
    login_page = LoginPage(driver)

    scenario = row.get("scenario", "")
    username = row.get("username", "")
    password = row.get("password", "")
    expected_error = row.get("expected_error", "")

    logger.info(
        f"[LOGIN NOK] Escenario: {scenario} | "
        f"username='{username}' password='{password}' | "
        f"Esperado error que contenga: '{expected_error}'"
    )

    # Guardamos datos en el nodo del test para que lleguen al reporte HTML si hace falta
    request.node.user_properties.append(("scenario", scenario))
    request.node.user_properties.append(("expected_error", expected_error))

    login_page.open_login_page(base_url)
    login_page.login(username, password)

    assert login_page.is_error_visible(), (
        f"[{scenario}] Esperado: que aparezca un mensaje de error. "
        f"Obtenido: NO se mostró ningún mensaje."
    )

    if expected_error:
        msg = login_page.get_error_message()
        logger.info(f"[LOGIN NOK] Mensaje mostrado: '{msg}'")

        assert expected_error in msg, (
            f"[{scenario}] Validación de mensaje de error.\n"
            f"  Esperado que contenga: '{expected_error}'\n"
            f"  Obtenido: '{msg}'"
        )
