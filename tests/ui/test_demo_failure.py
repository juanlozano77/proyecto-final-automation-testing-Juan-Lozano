# tests/ui/test_demo_failure.py

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_demo_ui_intentional_failure(driver, base_url, valid_users):
    """
    Caso de prueba INTENCIONALMENTE FALLIDO.

    Objetivo:
    - Demostrar cómo el framework se comporta ante un fallo:
      * Se genera screenshot.
      * El fallo queda registrado en el log.
      * El reporte HTML muestra el test en rojo con el mensaje de error.

    Escenario:
    - Login correcto con usuario válido.
    - Se verifica (a propósito) que exista un texto inexistente en la página.

    Este test NO representa un fallo funcional real de la aplicación,
    sino un caso artificial para mostrar las capacidades del framework.
    """

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    user = valid_users["standard_user"]
    logger.info("[DEMO FAIL] Iniciando test intencionalmente fallido de UI.")

    # Login normal (esto sí debería funcionar)
    login_page.open_login_page(base_url)
    login_page.login(user["username"], user["password"])

    assert inventory_page.is_loaded(), (
        "Precondición fallida: se esperaba poder acceder al inventario después del login."
    )

    # Aquí viene la parte intencionalmente incorrecta:
    texto_inexistente = "ESTE_TEXTO_NO_EXISTE_EN_LA_PAGINA"
    page_source = driver.page_source

    logger.info(
        f"[DEMO FAIL] Buscando texto inexistente en la página: '{texto_inexistente}'"
    )

    assert texto_inexistente in page_source, (
        "TEST DE DEMOSTRACIÓN DE FALLO.\n"
        f"  Esperado (a propósito): que la página contenga el texto: '{texto_inexistente}'.\n"
        "  Obtenido: ese texto NO está en la página.\n\n"
        "Este caso está diseñado para fallar y así mostrar:\n"
        "  - Captura automática de pantalla.\n"
        "  - Registro detallado en logs.\n"
        "  - Estado FAILED en el reporte HTML."
    )
