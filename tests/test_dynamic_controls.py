import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.dynamic_controls_page import DynamicControlsPage
from utils.logger import get_logger

logger = get_logger("TestDynamicControls")


@pytest.mark.dynamic_controls
def test_dynamic_controls(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: Dynamic Controls

    Verifies dynamic behavior of checkbox and input elements on the page.

    Test Steps:
    1. Open the Dynamic Controls page.
    2. Remove the checkbox and verify it disappears.
    3. Add the checkbox back and verify it appears.
    4. Enable the input field and verify it becomes editable.
    5. Type text into the input field.
    6. Disable the input field and verify it is no longer editable.

    Expected Results:
    - Checkbox can be dynamically removed and added.
    - Input field can be enabled, typed into, and disabled correctly.
    """
    page = DynamicControlsPage(driver, wait)
    logger.info("Starting dynamic controls test")

    # Open the Dynamic Controls page
    page.open()
    logger.debug("Dynamic Controls page opened successfully")

    # ---- Checkbox Tests ----
    page.remove_checkbox()
    assert not page.is_checkbox_present(), "Checkbox was not removed"
    logger.info("Checkbox removed successfully")

    page.add_checkbox()
    assert page.is_checkbox_present(), "Checkbox was not added"
    logger.info("Checkbox added successfully")

    # ---- Input Field Tests ----
    page.enable_input()
    assert page.is_input_enabled(), "Input field was not enabled"
    logger.info("Input field enabled successfully")

    page.type_in_input("Testing dynamic controls")
    logger.info("Typed text into input field")

    page.disable_input()
    assert not page.is_input_enabled(), "Input field was not disabled"
    logger.info("Input field disabled successfully")

    logger.info("Dynamic controls test completed successfully")
