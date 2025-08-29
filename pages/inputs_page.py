from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger
from selenium.common.exceptions import TimeoutException, WebDriverException


class InputsPage:
    """
    Page Object Model for the 'Inputs' page in 'The Internet' demo site.

    Attributes:
        URL (str): Full URL of the Inputs page.
        INPUT_FIELD (tuple): Locator tuple for the input field element.
    """


    URL: str = f"{CONFIG.get('base_url')}/inputs"
    INPUT_FIELD = (By.TAG_NAME, "input")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the InputsPage object with driver and wait objects.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Selenium WebDriverWait instance for explicit waits.
        """
        # WebDriver instance for browser interaction
        self.driver = driver
        # WebDriverWait instance for explicit waits
        self.wait = wait
        # Logger specific to this class
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Navigate to the Inputs page.

        Raises:
            WebDriverException: If the page fails to load.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def get_input_field(self) -> WebDriver:
        """
        Locate and return the input field element.

        Uses an explicit wait until the field is visible.

        Returns:
            WebElement: Input field element.

        Raises:
            TimeoutException: If the input field is not visible in time.
        """
        try:
            field = self.wait.until(EC.visibility_of_element_located(self.INPUT_FIELD))
            self.logger.debug("Input field located")
            return field
        except TimeoutException:
            self.logger.exception("Input field not visible in time")
            raise

    def clear_field(self) -> None:
        """
        Clear the content of the input field.

        Raises:
            WebDriverException: If the input field cannot be cleared.
        """
        try:
            # Ensure the field is visible before clearing
            field = self.get_input_field()
            field.clear()
            self.logger.debug("Cleared input field")
        except WebDriverException:
            self.logger.exception("Failed to clear input field")
            raise

    def type_value(self, value: str) -> None:
        """
        Type the given value into the input field.

        Args:
            value (str): The string to input.

        Raises:
            WebDriverException: If typing fails.
        """
        try:
            # Ensure the field is ready for input
            field = self.get_input_field()
            field.send_keys(value)
            self.logger.info("Typed value into input: %s", value)
        except WebDriverException:
            self.logger.exception("Failed to type value into input: %s", value)
            raise

    def type_each_char(self, value: str) -> None:
        """
        Type a string into the input field character by character.

        Simulates realistic typing behavior for testing dynamic input handling.

        Args:
            value (str): The string to type character by character.

        Raises:
            WebDriverException: If typing fails.
        """
        try:
            field = self.get_input_field()
            for key in value:
                field.send_keys(key)
                self.logger.debug("Typed char: %s", key)
            self.logger.info("Finished typing sequence: %s", value)
        except WebDriverException:
            self.logger.exception("Failed to type characters into input: %s", value)
            raise
