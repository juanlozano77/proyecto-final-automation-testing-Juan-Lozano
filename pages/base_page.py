from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Clase base para todas las páginas del framework.

    Encapsula las operaciones más comunes sobre elementos:
    - abrir una URL
    - encontrar elementos
    - hacer click
    - escribir texto
    - obtener texto
    - verificar visibilidad
    """

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        element = self.find(locator)
        element.click()

    def type(self, locator, text: str, clear_first: bool = True):
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        element = self.find(locator)
        return element.text

    def is_visible(self, locator) -> bool:
        try:
            self.find(locator)
            return True
        except Exception:
            return False
