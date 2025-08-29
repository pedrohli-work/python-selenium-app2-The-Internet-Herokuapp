from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger

class FramesPage:
    """
    Page Object for interacting with the Frames section of 'The Internet' app.

    This class focuses on testing text editing inside an iframe.
    It provides methods to open the frames page, navigate into the iframe,
    manipulate its body content, and switch context back to the main page.
    """


    URL = f"{CONFIG.get('base_url')}/frames"

    # Locators
    IFRAME_LINK = (By.LINK_TEXT, "iFrame")
    IFRAME_BODY = (By.CSS_SELECTOR, "body#tinymce")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the FramesPage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait handler.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Open the Frames page.

        Raises:
            WebDriverException: If the URL cannot be loaded.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def click_iframe_link(self) -> None:
        """
        Click the link that opens the iFrame editor.

        Raises:
            TimeoutException: If the iframe link is not clickable.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(self.IFRAME_LINK)).click()
            self.logger.info("Clicked iframe link")
        except TimeoutException:
            self.logger.exception("Timeout: Iframe link not clickable")
            raise

    def switch_to_iframe(self) -> None:
        """
        Switch Selenium's context into the iframe.

        Raises:
            TimeoutException: If the iframe is not found.
        """
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.ID, "mce_0_ifr")))
            self.driver.switch_to.frame(iframe)
            self.logger.info("Switched to iframe")
        except TimeoutException:
            self.logger.exception("Timeout: Iframe not found")
            raise

    def switch_to_default_content(self) -> None:
        """
        Switch Selenium's context back to the main page content.
        """
        self.driver.switch_to.default_content()
        self.logger.info("Switched back to default content")

    def clear_iframe_body(self) -> None:
        """
        Clear the body content inside the iframe.

        Raises:
            TimeoutException: If the iframe body is not found.
        """
        try:
            body = self.wait.until(EC.presence_of_element_located(self.IFRAME_BODY))
            self.driver.execute_script("arguments[0].innerHTML = '';", body)
            self.logger.info("Cleared iframe body")
        except TimeoutException:
            self.logger.exception("Timeout: Iframe body not found")
            raise

    def set_iframe_text(self, text: str) -> None:
        """
        Set custom text inside the iframe body using JavaScript.

        Args:
            text (str): The text to insert.

        Raises:
            TimeoutException: If the iframe body is not found.
        """
        try:
            body = self.wait.until(EC.presence_of_element_located(self.IFRAME_BODY))
            self.driver.execute_script("arguments[0].innerHTML = arguments[1];", body, text)
            self.logger.info("Set iframe text: %s", text)
        except TimeoutException:
            self.logger.exception("Timeout: Iframe body not found for setting text")
            raise

    def get_iframe_text(self) -> str:
        """
        Retrieve the current text from the iframe body.

        Returns:
            str: The text inside the iframe.

        Raises:
            TimeoutException: If the iframe body is not found.
        """
        try:
            body = self.wait.until(EC.presence_of_element_located(self.IFRAME_BODY))
            text = self.driver.execute_script("return arguments[0].innerText;", body)
            self.logger.info("Retrieved iframe text: %s", text)
            return text
        except TimeoutException:
            self.logger.exception("Timeout: Iframe body not found for getting text")
            raise