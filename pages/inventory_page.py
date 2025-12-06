from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .base_page import BasePage


class InventoryPage(BasePage):
    """Page Object para la página de inventario de productos."""

    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@data-test, 'add-to-cart')]")

    def is_loaded(self) -> bool:
        return self.is_visible(self.INVENTORY_CONTAINER)

    def add_first_product_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def get_cart_badge_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def get_all_prices(self):
        elements = self.driver.find_elements(*self.ITEM_PRICE)
        prices = []
        for e in elements:
            text = e.text.replace("$", "").strip()
            try:
                prices.append(float(text))
            except ValueError:
                continue
        return prices

    def sort_products(self, value: str):
        dropdown = self.find(self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(value)
