from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import get_logger

from selenium.webdriver.common.by import By

logger = get_logger(__name__)


def test_checkout_missing_first_name(driver, base_url, valid_users):
    """
    Caso de prueba negativo:
    Intentar avanzar en el checkout sin completar el campo First Name.

    Esperado:
    - El sistema NO debe permitir avanzar.
    - Debe mostrar el mensaje: "Error: First Name is required"
    """

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # ---- Login ----
    user = valid_users["standard_user"]
    login_page.open_login_page(base_url)
    login_page.login(user["username"], user["password"])
    assert inventory_page.is_loaded(), "No se pudo acceder al inventario después del login."

    # ---- Agregar producto ----
    inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()
    assert cart_page.get_items_count() >= 1, "El carrito está vacío en un test negativo."

    # ---- Ir a checkout ----
    cart_page.click_checkout()

    # ---- Dejar First Name vacío a propósito ----
    checkout_page.type(checkout_page.LAST_NAME, "Lozano")
    checkout_page.type(checkout_page.POSTAL_CODE, "1846")
    checkout_page.click(checkout_page.CONTINUE_BUTTON)

    # ---- Validar mensaje de error ----
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    assert checkout_page.is_visible(ERROR_MESSAGE), (
        "Esperado: mensaje de error porque falta el First Name.\n"
        "Obtenido: NO se mostró mensaje."
    )

    msg = checkout_page.get_text(ERROR_MESSAGE)
    logger.info(f"Mensaje de error mostrado: {msg}")

    assert "First Name is required" in msg, (
        "Validación de error en checkout.\n"
        "  Esperado: 'First Name is required'\n"
        f"  Obtenido: '{msg}'"
    )
