import pytest
from pages.frames_page import FramesPage
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from utils.logger import get_logger

logger = get_logger("TestFrames")


@pytest.mark.frames
def test_iframe_text_editing(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: iFrame Text Editing

    Verifies that text can be inserted, edited, and retrieved inside an iframe.

    Test Steps:
    1. Open the Frames page.
    2. Click the link to open the example iframe.
    3. Switch Selenium focus to the iframe.
    4. Clear the iframe body content.
    5. Set new text inside the iframe.
    6. Verify that the text was correctly inserted.
    7. Switch back to the default page content.

    Expected Results:
    - Text inserted inside the iframe matches exactly the input provided.
    - Selenium focus can switch to and from the iframe without errors.
    """
    page = FramesPage(driver, wait)
    logger.info("Starting iframe text editing test")

    # Open the Frames page
    page.open()
    logger.debug("Frames page opened successfully")

    # Click link to navigate to the iFrame example
    page.click_iframe_link()
    logger.debug("Clicked iframe link")

    # Switch context to iframe
    page.switch_to_iframe()
    logger.debug("Switched to iframe")

    # Clear iframe body and insert test text
    page.clear_iframe_body()
    test_text = "Hello, this is a test!"
    page.set_iframe_text(test_text)
    logger.info("Inserted test text into iframe")

    # Retrieve and verify the text inside the iframe
    actual_text = page.get_iframe_text()
    assert actual_text == test_text, "Text input inside iframe failed!"
    logger.info("Iframe text verified successfully")

    # Switch back to main content
    page.switch_to_default_content()
    logger.info("Iframe text editing test completed successfully")
