from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger

class WindowsPage:
    """
    Page Object representing the 'Multiple Windows' page of the application.
    
    Provides methods to:
    - open the page,
    - click the link that opens a new window,
    - switch between windows,
    - retrieve heading text,
    - and close windows.
    """


    URL = f"{CONFIG.get('base_url')}/windows"

    # Locators
    CLICK_HERE_LINK = (By.LINK_TEXT, "Click Here")
    HEADING = (By.TAG_NAME, "h3")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the WindowsPage object.
        
        :param driver: Instance of Selenium WebDriver.
        :param wait: Instance of WebDriverWait for explicit waits.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Open the Multiple Windows page.
        
        :raises WebDriverException: If the page fails to load.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def click_new_window_link(self) -> None:
        """
        Click the 'Click Here' link to open a new window 
        and wait until the new window handle appears.
        
        :raises TimeoutException: If the link cannot be clicked or 
                                  the new window does not appear in time.
        """
        try:
            self.wait.until(EC.element_to_be_clickable(self.CLICK_HERE_LINK)).click()
            self.wait.until(lambda d: len(d.window_handles) > 1)
            self.logger.info("Clicked 'Click Here' link to open new window")
        except TimeoutException:
            self.logger.exception("Timeout while clicking 'Click Here' link")
            raise

    def switch_to_new_window(self) -> None:
        """
        Switch WebDriver focus to the newly opened window.
        
        :raises RuntimeError: If no new window is found.
        """
        original_window = self.driver.current_window_handle
        for handle in self.driver.window_handles:
            if handle != original_window:
                self.driver.switch_to.window(handle)
                self.logger.info("Switched to new window")
                return
        self.logger.error("New window not found")
        raise RuntimeError("New window not found")

    def get_heading_text(self) -> str:
        """
        Retrieve the text of the <h3> element in the current window.
        
        :return: The heading text.
        :raises TimeoutException: If the heading is not found within the timeout.
        """
        try:
            heading = self.wait.until(EC.presence_of_element_located(self.HEADING))
            self.logger.info("Heading text in current window: %s", heading.text)
            return heading.text
        except TimeoutException:
            self.logger.exception("Timeout while waiting for heading in window")
            raise

    def close_current_window(self) -> None:
        """
        Close the current browser window.
        """
        self.driver.close()
        self.logger.info("Closed current window")

    def switch_to_window(self, handle: str) -> None:
        """
        Switch focus back to a specific window by its handle.
        
        :param handle: The window handle to switch to.
        """
        self.driver.switch_to.window(handle)
        self.logger.info("Switched back to window: %s", handle)
