import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPage
from utils.config_loader import CONFIG
from utils.logger import get_logger

# Dedicated logger for login tests
logger = get_logger("TestLogin")


@pytest.mark.login
def test_login_positive(driver: WebDriver, wait: WebDriverWait):
    """
    Test Case: Positive Login

    Verifies that a user can log in with valid credentials.

    Steps:
    1. Open the login page.
    2. Enter valid username and password.
    3. Submit the login form.
    4. Verify that the success flash message is displayed.

    Expected Result:
    A success message "You logged into a secure area!" should be shown.
    """
    login_page = LoginPage(driver, wait)
    logger.info("Starting positive login test")

    # Open the login page
    login_page.open()
    logger.debug("Login page opened successfully")

    # Perform login with valid credentials from configuration
    login_page.login(CONFIG["credentials"]["username"], CONFIG["credentials"]["password"])

    # Retrieve and validate flash message
    flash = login_page.get_flash_message()
    logger.info("Flash message received: %s", flash)

    assert "You logged into a secure area!" in flash, \
        "Success message not shown after valid login"
    
    logger.info("Positive login test passed")


@pytest.mark.login
def test_login_negative(driver: WebDriver, wait: WebDriverWait):
    """
    Test Case: Negative Login

    Verifies that the system displays an error message when invalid 
    credentials are used.

    Steps:
    1. Open the login page.
    2. Enter invalid username and password.
    3. Submit the login form.
    4. Verify that an error flash message is displayed.

    Expected Result:
    An error message ("Your username is invalid!" or 
    "Your password is invalid!") should be shown.
    """
    login_page = LoginPage(driver, wait)
    logger.info("Starting negative login test")
    
    # Open the login page
    login_page.open()

    # Perform login with invalid credentials
    login_page.login("wronguser", "wrongpassword")

    # Retrieve and validate flash message
    flash = login_page.get_flash_message()
    logger.info("Flash message received: %s", flash)

    assert "Your username is invalid!" in flash or "Your password is invalid!" in flash, \
    "Error message not shown after  invalid login"

    logger.info("Negative login test passed")
