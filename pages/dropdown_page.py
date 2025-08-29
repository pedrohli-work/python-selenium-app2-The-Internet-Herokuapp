from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from utils.config_loader import CONFIG
from utils.logger import get_logger


class DropdownPage:
    """
    Page Object Model for the 'Dropdown' page in 'The Internet' demo site.

    Attributes:
        URL (str): Full URL for the dropdown page.
        DROPDOWN (tuple): Locator for the dropdown element.
    """
     
    
    URL = f"{CONFIG.get('base_url')}/dropdown"
    DROPDOWN = (By.ID, "dropdown")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the DropdownPage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait instance for synchronization.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def get_dropdown_element(self) -> 'Select':
        """
        Locate and return the dropdown element wrapped in a Select object.

        Returns:
            Select: Selenium Select object for interacting with the dropdown.

        Raises:
            TimeoutException: If the dropdown is not found within the timeout.
        """
        try:
            elem = self.wait.until(EC.visibility_of_element_located(self.DROPDOWN))
            self.logger.debug("Dropdown element located")
            return Select(elem)
        except TimeoutException:
            self.logger.exception("Timeout: Dropdown element not found")
            raise

    def select_by_visible_text(self, text: str) -> None:
        """
        Select an option in the dropdown by its visible text.

        Args:
            text (str): The visible text of the option to select.
        """
        dropdown = self.get_dropdown_element()
        dropdown.select_by_visible_text(text)
        self.logger.info("Selected dropdown option by text: %s", text)

    def select_by_value(self, value: str) -> None:
        """
        Select an option in the dropdown by its value attribute.

        Args:
            value (str): The value attribute of the option to select.
        """
        dropdown = self.get_dropdown_element()
        dropdown.select_by_value(value)
        self.logger.info("Selected dropdown option by value: %s", value)

    def get_selected_option(self) -> str:
        """
        Get the currently selected option from the dropdown.

        Returns:
            str: The text of the currently selected option.
        """
        dropdown = self.get_dropdown_element()
        selected = dropdown.first_selected_option.text
        self.logger.debug("Current selected option: %s", selected)
        return selected