from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger


class CheckboxesPage:
    """
    Page Object Model for the 'Checkboxes' page in 'The Internet' demo site.

    Attributes:
        URL (str): Full URL for the checkboxes page.
        CHECKBOXES_INPUT (tuple): Locator for all checkboxes on the page.
    """


    URL = f"{CONFIG.get('base_url')}/checkboxes"
    CHECKBOXES_INPUT = (By.CSS_SELECTOR, "input[type='checkbox']")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the CheckboxesPage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait instance for synchronization.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Navigate to the checkboxes page.

        Raises:
            WebDriverException: If the page cannot be opened.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def get_checkboxes(self) -> List[WebElement]:
        """
        Locate all checkboxes on the page.

        Returns:
            List[WebElement]: List of located checkbox elements.

        Raises:
            TimeoutException: If no checkbox is found within the timeout.
        """
        try:
            boxes = self.wait.until(
                EC.visibility_of_all_elements_located(self.CHECKBOXES_INPUT)
                )
            self.logger.debug("Located %d checkbox(es)", len(boxes))
            return boxes
        except TimeoutException:
            self.logger.exception("Timeout: Checkbox not found")
            raise

    def mark_all(self) -> None:
        """
        Select (check) all checkboxes that are not already selected.

        Logs how many checkboxes were marked.
        """
        boxes = self.get_checkboxes()
        to_mark = [cb for cb in boxes if not cb.is_selected()]
        for cb in to_mark:
            cb.click()
        self.logger.info("Marked %d checkbox(es)", len(to_mark))

    def unmark_all(self):
        """
        Unselect (uncheck) all checkboxes that are currently selected.

        Logs how many checkboxes were unmarked.
        """
        boxes = self.get_checkboxes()
        to_unmark = [cb for cb in boxes if cb.is_selected()]
        for cb in to_unmark:
            cb.click()
        self.logger.info("Unmarked %d checkbox(es)", len(to_unmark))

    def are_all_marked(self) -> bool:
        """
        Verify if all checkboxes are selected.

        Returns:
            bool: True if all checkboxes are checked, False otherwise.
        """
        return all(cb.is_selected() for cb in self.get_checkboxes())
    
    def are_all_unmarked(self) -> bool:
        """
        Verify if all checkboxes are unselected.

        Returns:
            bool: True if all checkboxes are unchecked, False otherwise.
        """
        return all(not cb.is_selected() for cb in self.get_checkboxes())