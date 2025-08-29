import pytest
import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.file_upload_page import FileUploadPage
from utils.logger import get_logger

# Dedicated logger for file upload tests
logger = get_logger("TestFileUpload")


@pytest.mark.fileupload
def test_file_upload(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: File Upload Page Functionality

    Verifies that a file can be uploaded successfully and that
    the page displays a confirmation message upon successful upload.

    Test Scenarios:
    1. Navigate to the File Upload page.
    2. Select a file to upload.
    3. Click the upload button.
    4. Verify that the success message is displayed.

    Expected Results:
    - File is uploaded successfully.
    - "File Uploaded!" message is visible on the page.
    """
    page = FileUploadPage(driver, wait)
    logger.info("Opening File Upload page")

    # Open the File Upload page
    page.open()
    logger.debug("File Upload page opened successfully")

    # ---- Test: Upload a file ----
    # Absolute path to the file to upload
    file_path = os.path.abspath(r"C:\Users\pedrohli\Documents\GIT_commit.txt")
    logger.info("Uploading file: %s", file_path)
    page.upload_file(file_path)

    # ---- Verification: Confirm upload success ----
    uploaded_text = page.get_uploaded_text()
    assert "File Uploaded!" in uploaded_text, "Upload confirmation message not found."
    logger.info("File uploaded successfully and confirmed")
