from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import get_logger

logger = get_logger(__name__)


def login_as_standard_user(driver, base_url, valid_users):
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)

    user = valid_users["standard_user"]
    login_page.open_login_page(base_url)
    login_page.login(user["username"], user["password"])
    assert inventory_page.is_loaded(), "No se pudo acceder al inventario."
    return inventory_page


def test_add_product_to_cart(driver, base_url, valid_users):
    """Login -> agregar producto al carrito -> validar contador en el ícono del carrito."""
    inventory_page = login_as_standard_user(driver, base_url, valid_users)

    initial_count = inventory_page.get_cart_badge_count()
    inventory_page.add_first_product_to_cart()
    new_count = inventory_page.get_cart_badge_count()

    logger.info(f"Carrito pasó de {initial_count} a {new_count}")
    assert new_count == initial_count + 1, "El contador del carrito no se incrementó correctamente."


def test_sort_products_high_to_low(driver, base_url, valid_users):
    """Login -> ordenar productos de mayor a menor precio -> validar orden."""
    inventory_page = login_as_standard_user(driver, base_url, valid_users)

    inventory_page.sort_products("hilo")  # high to low
    prices = inventory_page.get_all_prices()
    logger.info(f"Precios obtenidos: {prices}")

    assert prices == sorted(prices, reverse=True), "Los productos no están ordenados de mayor a menor precio."
