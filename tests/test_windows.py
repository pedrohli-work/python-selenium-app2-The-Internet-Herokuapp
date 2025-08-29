import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.windows_page import WindowsPage
from utils.logger import get_logger

logger = get_logger("TestWindows")


@pytest.mark.windows
def test_multiple_windows(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: Multiple Windows Handling

    Verifies the behavior of opening a new window and switching between windows.

    Test Steps:
    1. Open the Windows page.
    2. Store the handle of the original window.
    3. Click the link that opens a new window.
    4. Switch focus to the new window and verify the heading text.
    5. Close the new window.
    6. Switch back to the original window and verify the focus.

    Expected Results:
    - New window opens successfully and can be focused.
    - Heading text in new window matches expected value.
    - Focus returns to original window after closing the new one.
    """
    page = WindowsPage(driver, wait)
    logger.info("Starting multiple windows test")

    # Open the Windows page
    page.open()
    logger.debug("Windows page opened successfully")

    # Store original window handle
    original_window = driver.current_window_handle
    logger.debug("Stored original window handle: %s", original_window)

    # ---- Open and switch to new window ----
    page.click_new_window_link()
    page.switch_to_new_window()
    logger.info("Switched to newly opened window")

    # Verify heading text in the new window
    heading = page.get_heading_text()
    assert heading == "New Window", f"Expected heading 'New Window', got '{heading}'"
    logger.info("Heading text verified successfully in new window")

    # Close the new window and return to original window
    page.close_current_window()
    page.switch_to_window(original_window)
    assert driver.current_window_handle == original_window, "Did not switch back to original window"
    logger.info("Switched back to original window successfully")

    logger.info("Multiple windows test completed successfully")
