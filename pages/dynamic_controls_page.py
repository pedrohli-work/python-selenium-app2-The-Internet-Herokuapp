from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger

class DynamicControlsPage:
    """
    Page Object for testing dynamic controls page.
    Includes interactions with checkbox (add/remove) 
    and input field (enable/disable).
    """


    URL = f"{CONFIG.get('base_url')}/dynamic_controls"

    # Locators
    REMOVE_BUTTON = (By.XPATH, "//button[text()='Remove']")
    ADD_BUTTON = (By.XPATH, "//button[text()='Add']")
    CHECKBOX = (By.ID, "checkbox")
    ENABLE_BUTTON = (By.XPATH, "//button[text()='Enable']")
    DISABLE_BUTTON = (By.XPATH, "//button[text()='Disable']")
    INPUT_FIELD = (By.CSS_SELECTOR, "input[type='text']")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Class constructor.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait instance.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """Open the Dynamic Controls page."""
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def remove_checkbox(self) -> None:
        """Click 'Remove' button and wait until checkbox disappears."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.REMOVE_BUTTON)).click()
            self.wait.until(EC.invisibility_of_element_located(self.CHECKBOX))
            self.logger.info("Checkbox removed")
        except TimeoutException:
            self.logger.exception("Timeout while removing checkbox")
            raise

    def add_checkbox(self) -> None:
        """Click 'Add' button and wait until checkbox reappears."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).click()
            self.wait.until(EC.presence_of_element_located(self.CHECKBOX))
            self.logger.info("Checkbox added")
        except TimeoutException:
            self.logger.exception("Timeout while adding checkbox")
            raise

    def enable_input(self) -> None:
        """Click 'Enable' button and wait until input field is clickable."""
        try:
            self.driver.find_element(*self.ENABLE_BUTTON).click()
            self.wait.until(EC.element_to_be_clickable(self.INPUT_FIELD))
            self.logger.info("Input enabled")
        except TimeoutException:
            self.logger.exception("Timeout while enabling input")
            raise

    def type_in_input(self, text: str) -> None:
        """
        Clear the input field and type provided text.

        Args:
            text (str): Text to type into the input field.
        """
        input_field = self.wait.until(EC.element_to_be_clickable(self.INPUT_FIELD))
        input_field.clear()
        input_field.send_keys(text)
        self.logger.info("Typed in input: %s", text)

    def disable_input(self) -> None:
        """Click 'Disable' button and wait until input field is disabled."""
        try:
            self.driver.find_element(*self.DISABLE_BUTTON).click()
            self.wait.until(lambda d: self.driver.find_element(*self.INPUT_FIELD).get_attribute("disabled"))
            self.logger.info("Input disabled")
        except TimeoutException:
            self.logger.exception("Timeout while disabling input")
            raise

    def is_checkbox_present(self) -> bool:
        """
        Check if the checkbox is present in the DOM.

        Returns:
            bool: True if present, False otherwise.
        """
        return len(self.driver.find_elements(*self.CHECKBOX)) > 0

    def is_input_enabled(self) -> bool:
        """
        Check if the input field is enabled.

        Returns:
            bool: True if enabled, False if disabled.
        """
        return self.driver.find_element(*self.INPUT_FIELD).get_attribute("disabled") is None
