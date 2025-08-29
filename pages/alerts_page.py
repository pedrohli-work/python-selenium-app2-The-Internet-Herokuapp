from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger

class AlertsPage:
    """
    Page Object Model for the 'JavaScript Alerts' page in 'The Internet' demo site.

    Attributes:
        URL (str): Full URL for the alerts page.
        JS_ALERT_BUTTON (tuple): Locator for the "Click for JS Alert" button.
        JS_CONFIRM_BUTTON (tuple): Locator for the "Click for JS Confirm" button.
        JS_PROMPT_BUTTON (tuple): Locator for the "Click for JS Prompt" button.
        RESULT_TEXT (tuple): Locator for the text result element after alert actions.
    """


    URL = f"{CONFIG.get('base_url')}/javascript_alerts"

    JS_ALERT_BUTTON = (By.XPATH, "//button[text()='Click for JS Alert']")
    JS_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Click for JS Confirm']")
    JS_PROMPT_BUTTON = (By.XPATH, "//button[text()='Click for JS Prompt']")
    RESULT_TEXT = (By.ID, "result")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the AlertsPage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait instance for synchronization.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Navigate to the alerts page.

        Raises:
            WebDriverException: If the URL cannot be loaded.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def click_alert_button(self) -> None:
        """
        Click the "JS Alert" button to trigger a simple alert.

        Raises:
            TimeoutException: If the button is not clickable.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(self.JS_ALERT_BUTTON)).click()
            self.logger.info("Clicked JS Alert button")
        except TimeoutException:
            self.logger.exception("Timeout: JS Alert button not clickable")
            raise

    def click_confirm_button(self) -> None:
        """
        Click the "JS Confirm" button to trigger a confirmation alert.

        Raises:
            TimeoutException: If the button is not clickable.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(self.JS_CONFIRM_BUTTON)).click()
            self.logger.info("Clicked JS Confirm button")
        except TimeoutException:
            self.logger.exception("Timeout: JS Confirm button not clickable")
            raise

    def click_prompt_button(self) -> None:
        """
        Click the "JS Prompt" button to trigger a prompt alert.

        Raises:
            TimeoutException: If the button is not clickable.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(self.JS_PROMPT_BUTTON)).click()
            self.logger.info("Clicked JS Prompt button")
        except TimeoutException:
            self.logger.exception("Timeout: JS Prompt button not clickable")
            raise

    def accept_alert(self) -> None:
        """
        Accept the currently active alert.

        Raises:
            Exception: If switching to or accepting the alert fails.
        """
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            self.logger.info("Accepted alert")
        except Exception:
            self.logger.exception("Failed to accept alert")
            raise

    def dismiss_alert(self) -> None:
        """
        Dismiss the currently active alert.

        Raises:
            Exception: If switching to or dismissing the alert fails.
        """
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            self.logger.info("Dismissed alert")
        except Exception:
            self.logger.exception("Failed to dismiss alert")
            raise

    def send_keys_to_alert(self, text: str) -> None:
        """
        Send input text to the active prompt alert.

        Args:
            text (str): Text to send to the alert.

        Raises:
            Exception: If switching to the alert or sending keys fails.
        """
        try:
            alert = self.driver.switch_to.alert
            alert.send_keys(text)
            self.logger.info("Sent keys to prompt alert: %s", text)
        except Exception:
            self.logger.exception("Failed to send keys to alert")
            raise

    def get_alert_text(self) -> str:
        """
        Retrieve the text of the active alert.

        Returns:
            str: The alert message.

        Raises:
            Exception: If switching to or retrieving the text fails.
        """
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            self.logger.info("Retrieved alert text: %s", text)
            return text
        except Exception:
            self.logger.exception("Failed to retrieve alert text")
            raise

    def get_result_text(self) -> str:
        """
        Retrieve the result text displayed on the page after alert actions.

        Returns:
            str: Result text shown in the page.

        Raises:
            TimeoutException: If the result text element is not found or visible.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.RESULT_TEXT))
            text = element.text
            self.logger.info("Retrieved result text: %s", text)
            return text
        except TimeoutException:
            self.logger.exception("Timeout: Result text not found")
            raise
