import os
import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.data_loader import load_users_from_json
from utils.logger import get_logger

BASE_URL = "https://www.saucedemo.com/"
logger = get_logger(__name__)

# Directorios de salida
os.makedirs("screenshots", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def valid_users():
    """Carga usuarios válidos desde JSON."""
    return load_users_from_json("resources/test_data/users.json")


@pytest.fixture(scope="function")
def driver():
    logger.info("Iniciando WebDriver (Chrome)")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # activar si se quiere modo headless

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    logger.info("Cerrando WebDriver")
    driver.quit()


def pytest_configure(config):
    if hasattr(config, "_metadata"):
        config._metadata["Proyecto"] = "Trabajo Final Integrador - Automation Testing"
        config._metadata["Aplicación UI"] = "SauceDemo"
        config._metadata["API"] = "ReqRes"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura screenshots automáticamente cuando un test falla."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver is not None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            filename = os.path.join("screenshots", f"{test_name}_{timestamp}.png")
            driver.save_screenshot(filename)
            logger.error(f"Test {test_name} falló. Screenshot guardado en {filename}")

            # Adjuntar a reporte HTML si pytest-html está activo
            if item.config.pluginmanager.hasplugin("html"):
                from pytest_html import extras
                extra = getattr(rep, "extra", [])
                extra.append(extras.image(filename))
                rep.extra = extra

