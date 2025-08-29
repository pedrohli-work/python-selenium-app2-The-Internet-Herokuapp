from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger


class LoginPage:
    """
    Page Object Model (POM) for the login page of 'The Internet' website.

    Attributes:
        URL (str): Full URL of the login page.
        USERNAME_INPUT (tuple): Locator for username input field.
        PASSWORD_INPUT (tuple): Locator for password input field.
        LOGIN_BUTTON (tuple): Locator for login button.
        FLASH_MESSAGE (tuple): Locator for flash messages displayed after login.
    """


    URL = f"{CONFIG.get('base_url')}/login"

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.radius")
    FLASH_MESSAGE = (By.ID, "flash")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initializes the LoginPage instance.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Selenium WebDriverWait instance for explicit waits.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)
    
    def open(self) -> None:
        """
        Opens the login page using the configured URL.

        Raises:
            WebDriverException: If the page fails to load.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise
    
    def enter_username(self, username: str) -> None:
        """
        Enters the provided username into the username input field.

        Args:
            username (str): The username to input.

        Raises:
            TimeoutException: If the username field is not visible.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
            self.logger.debug("Entered username: %s", username)
        except TimeoutException:
            self.logger.exception("Timeout: Username field not found")
            raise

    def enter_password(self, password: str) -> None:
        """
        Enters the provided password into the password input field.

        Args:
            password (str): The password to input.

        Raises:
            TimeoutException: If the password field is not visible.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT)).send_keys(password)
            # Mask password in logs for security
            self.logger.info("Entered password: %s", '*' * len(password))
        except TimeoutException:
            self.logger.exception("Timeout: Password field not found")
            raise
    
    def click_login(self) -> None:
        """
        Clicks the login button to submit the login form.

        Raises:
            TimeoutException: If the login button is not clickable.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
            self.logger.info("Clicked login button")
        except TimeoutException:
            self.logger.exception("Timeout: Login button not clickable")
            raise

    def get_flash_message(self) -> str:
        """
        Retrieves the flash message displayed after login attempt.

        Returns:
            str: Flash message text, stripped of extra characters.

        Raises:
            TimeoutException: If the flash message is not found.
        """
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.FLASH_MESSAGE)).text
            # Remove trailing close button character ('x') and whitespace
            msg = msg.replace("x", "").strip()
            self.logger.info("Flash message retrieved: %s", msg)
            return msg
        except TimeoutException:
            self.logger.exception("Timeout: Flash message not found")
            raise

    def login(self, username: str, password: str) -> None:
        """
        Convenience method to perform a full login flow:
        enter username, enter password, click login.

        Args:
            username (str): Username for login.
            password (str): Password for login.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
