from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.config_loader import CONFIG
from utils.logger import get_logger

class FileUploadPage:
    """
    Page Object Model for the 'File Upload' page in 'The Internet' demo site.

    Attributes:
        URL (str): Full URL for the file upload page.
        FILE_INPUT (tuple): Locator for the file input element.
        UPLOAD_BUTTON (tuple): Locator for the upload button.
        UPLOADED_TEXT (tuple): Locator for the text shown after upload.
    """


    URL = f"{CONFIG.get('base_url')}/upload"

    FILE_INPUT = (By.ID, "file-upload")
    UPLOAD_BUTTON = (By.ID, "file-submit")
    UPLOADED_TEXT = (By.TAG_NAME, "h3")

    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        """
        Initialize the FileUploadPage object.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait instance for synchronization.
        """
        self.driver = driver
        self.wait = wait
        self.logger = get_logger(self.__class__.__name__)

    def open(self) -> None:
        """
        Navigate to the file upload page.

        Raises:
            WebDriverException: If the URL cannot be loaded.
        """
        try:
            self.driver.get(self.URL)
            self.logger.info("Opened URL: %s", self.URL)
        except WebDriverException:
            self.logger.exception("Failed to open URL: %s", self.URL)
            raise

    def upload_file(self, file_path: str) -> None:
        """
        Upload a file by sending the path to the file input and clicking submit.

        Args:
            file_path (str): Full local path of the file to be uploaded.

        Raises:
            TimeoutException: If file input or upload button are not interactable.
        """
        try:
            input_elem = self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
            input_elem.send_keys(file_path)
            self.logger.info("File path sent to input")
            button = self.wait.until(EC.element_to_be_clickable(self.UPLOAD_BUTTON))
            button.click()
            self.logger.info("Upload button clicked")
        except TimeoutException:
            self.logger.exception("Timeout during file upload")
            raise

    def get_uploaded_text(self) -> str:
        """
        Retrieve the confirmation text displayed after upload.

        Returns:
            str: Confirmation message (usually 'File Uploaded!').

        Raises:
            TimeoutException: If the confirmation text is not visible.
        """
        try:
            text_elem = self.wait.until(EC.visibility_of_element_located(self.UPLOADED_TEXT))
            msg = text_elem.text.strip()
            self.logger.info("Retrieved uploaded text: %s", msg)
            return msg
        except TimeoutException:
            self.logger.exception("Timeout: Uploaded text not found")
            raise
