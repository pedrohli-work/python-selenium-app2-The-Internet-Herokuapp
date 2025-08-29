from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os

def test_file_upload(driver_setup):
    """
    Test uploading a file and verifying the success confirmation on the page.
    """

    driver, wait = driver_setup

    # Absolute path to the file to upload
    file_path = os.path.abspath(r"C:\Users\pedrohli\Documents\GIT_commit.txt")

    # Navigate to the file upload page
    driver.get("https://the-internet.herokuapp.com/upload")

    # Wait for the file input element to appear and send the file path
    upload_input = wait.until(EC.presence_of_element_located((By.ID, "file-upload")))
    upload_input.send_keys(file_path)

    # Click the submit button to upload the file
    upload_button = wait.until(EC.element_to_be_clickable((By.ID, "file-submit")))
    upload_button.click()

    # Wait for the success message to appear and verify it
    uploaded_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert "File Uploaded!" in uploaded_text.text, "Upload confirmation message not found."
