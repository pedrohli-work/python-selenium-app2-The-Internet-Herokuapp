from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger

class DragAndDropPage:
    """
    Page Object representing the 'Drag and Drop' page of the application.

    Provides methods to:
    - open the page,
    - perform drag-and-drop between elements,
    - retrieve box headers after the operation.
    """


    URL = f"{CONFIG.get('base_url')}/drag_and_drop"

    # Locators
    BOX_A = (By.ID, "column-a")
    BOX_B = (By.ID, "column-b")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the DragAndDropPage object.

        :param driver: Instance of Selenium WebDriver.
        :param wait: Instance of WebDriverWait for explicit waits.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Open the Drag and Drop page.

        :raises WebDriverException: If the page fails to load.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def drag_and_drop_boxes(self) -> None:
        """
        Perform drag-and-drop from Box A to Box B.

        :raises TimeoutException: If either box is not found within the timeout.
        :raises WebDriverException: If the drag-and-drop action fails.
        """
        try:
            box_a = self.wait.until(EC.presence_of_element_located(self.BOX_A))
            box_b = self.wait.until(EC.presence_of_element_located(self.BOX_B))

            # Create and execute drag-and-drop action
            actions = ActionChains(self.driver)
            actions.drag_and_drop(box_a, box_b).perform()

            self.logger.info("Performed drag and drop from Box A to Box B")
        except TimeoutException:
            self.logger.exception("Timeout while locating boxes for drag and drop")
            raise
        except WebDriverException:
            self.logger.exception("Failed to perform drag and drop action")
            raise

    def get_box_headers(self) -> tuple[str, str]:
        """
        Retrieve the current headers of Box A and Box B after drag-and-drop.

        :return: Tuple with header texts (header_a, header_b).
        :raises WebDriverException: If headers cannot be retrieved.
        """
        try:
            box_a = self.driver.find_element(*self.BOX_A)
            box_b = self.driver.find_element(*self.BOX_B)

            # Extract header text from both boxes
            header_a = box_a.find_element(By.TAG_NAME, "header").text
            header_b = box_b.find_element(By.TAG_NAME, "header").text

            self.logger.info("Box headers: A='%s', B='%s'", header_a, header_b)
            return header_a, header_b
        except WebDriverException:
            self.logger.exception("Failed to retrieve box headers")
            raise
