from selenium.webdriver.common.by import By

from .base_page import BasePage


class CartPage(BasePage):
    """Page Object para el carrito de compras."""

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_items_count(self) -> int:
        items = self.driver.find_elements(*self.CART_ITEM)
        return len(items)

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
