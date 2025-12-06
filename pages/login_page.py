from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object para la pantalla de login de SauceDemo."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open_login_page(self, base_url: str):
        self.open(base_url)

    def login(self, username: str, password: str):
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)
