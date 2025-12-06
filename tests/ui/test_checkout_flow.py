from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import get_logger

logger = get_logger(__name__)


def test_complete_checkout_flow(driver, base_url, valid_users):
    """Flujo completo: login -> agregar producto -> carrito -> checkout -> finalizar compra."""
    user = valid_users["standard_user"]

    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)
    checkout_page = CheckoutPage(driver)

    # Login
    login_page.open_login_page(base_url)
    login_page.login(user["username"], user["password"])
    assert inventory_page.is_loaded(), "No se pudo acceder al inventario después del login."

    # Agregar producto y navegar al carrito
    inventory_page.add_first_product_to_cart()
    inventory_page.go_to_cart()
    assert cart_page.get_items_count() >= 1, "El carrito está vacío y debería tener al menos un ítem."

    # Checkout
    cart_page.click_checkout()
    checkout_page.fill_customer_info("Juan", "Lozano", "1846")
    checkout_page.finish_order()

    msg = checkout_page.get_success_message()
    logger.info(f"Mensaje de éxito en checkout: {msg}")

    assert "THANK YOU" in msg.upper(), "No se mostró el mensaje de confirmación de compra."
