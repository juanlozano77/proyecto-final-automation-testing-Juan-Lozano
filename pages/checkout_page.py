from selenium.webdriver.common.by import By

from .base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object para el flujo de checkout."""

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "complete-header")

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def finish_order(self):
        self.click(self.FINISH_BUTTON)

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MESSAGE)
