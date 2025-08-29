import pytest
from pages.alerts_page import AlertsPage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.logger import get_logger

# Dedicated logger for JavaScript alerts tests
logger = get_logger("TestAlerts")


@pytest.mark.alerts
def test_javascript_alerts(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: JavaScript Alerts Handling

    Verifies behavior and handling of JavaScript alerts on the 'Alerts' page.

    Test Scenarios:
    1. Open a simple JS alert and accept it.
    2. Open a JS confirm alert and dismiss it.
    3. Open a JS prompt alert, input text, and accept it.
    4. Verify that the result message reflects prompt input correctly.

    Expected Results:
    - Alert, confirm, and prompt alerts display correct messages.
    - Prompt input is correctly registered and displayed on the page.
    """
    page = AlertsPage(driver, wait)
    logger.info("Starting JS Alerts test")

    # Open the Alerts page
    page.open()
    logger.debug("Alerts page opened successfully")

    # ---- Test 1: Simple alert ----
    page.click_alert_button()
    assert page.get_alert_text() == "I am a JS Alert", "Unexpected JS Alert text"
    page.accept_alert()

    # ---- Test 2: Confirm alert ----
    page.click_confirm_button()
    assert page.get_alert_text() == "I am a JS Confirm", "Unexpected JS Confirm text"
    page.dismiss_alert()

    # ---- Test 3: Prompt alert ----
    page.click_prompt_button()
    assert page.get_alert_text() == "I am a JS prompt", "Unexpected JS Prompt text"
    page.send_keys_to_alert("Pedro was here!")
    page.accept_alert()

    # Verificar mensagem de resultado
    result = page.get_result_text()
    assert "You entered: Pedro was here!" in result, "Prompt input was not registered correctly"
    logger.info("JS Alerts test completed successfully")
