import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.dropdown_page import DropdownPage
from utils.logger import get_logger

# Dedicated logger for dropdown tests
logger = get_logger("TestDropdown")


@pytest.mark.dropdown
def test_dropdown(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: Dropdown Page Functionality

    Verifies the ability to select options from the dropdown using
    both visible text and value attribute.

    Test Scenarios:
    1. Select option by visible text → the correct option should be selected.
    2. Select option by value → the correct option should be selected.

    Expected Results:
    - Selecting by visible text updates the dropdown selection correctly.
    - Selecting by value updates the dropdown selection correctly.
    """
    page = DropdownPage(driver, wait)
    logger.info("Starting dropdown test")

    # Open the Dropdown page
    page.open()
    logger.debug("Dropdown page opened successfully")

    # ---- Test 1: Select "Option 1" by visible text ----
    page.select_by_visible_text("Option 1")
    selected = page.get_selected_option()
    assert selected == "Option 1", f"Expected 'Option 1', got '{selected}'"
    logger.info("Option 1 selected successfully")

    # ---- Test 2: Select "Option 2" by value ----
    page.select_by_value("2")
    selected = page.get_selected_option()
    assert selected == "Option 2", f"Expected 'Option 2', got '{selected}'"
    logger.info("Option 2 selected successfully")

    logger.info("Dropdown test completed successfully")
