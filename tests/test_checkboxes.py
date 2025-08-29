import pytest
from pages.checkboxes_page import CheckboxesPage
from utils.logger import get_logger
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

# Dedicated logger for checkboxes tests
logger = get_logger("TestCheckboxes")


@pytest.mark.checkboxes
def test_checkboxes(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: Checkboxes Page Functionality

    Verifies the ability to mark and unmark all checkboxes on the Checkboxes page.

    Test Scenarios:
    1. Mark all checkboxes → all checkboxes should be selected.
    2. Unmark all checkboxes → all checkboxes should be deselected.

    Expected Results:
    - All checkboxes are correctly marked when marking.
    - All checkboxes are correctly unmarked when unmarking.
    """
    page  = CheckboxesPage(driver, wait)
    logger.info("Starting checkboxes test")

    # Open the Checkboxes page
    page.open()
    logger.debug("Checkboxes page opened successfully")

    # ---- Test 1: Mark all checkboxes ----
    logger.debug("Marking all checkboxes...")
    page.mark_all()
    assert page.are_all_marked(), "Not all checkboxes were marked"
    logger.info("All checkboxes marked successfully")

    # ---- Test 2: Unmark all checkboxes ----
    logger.debug("Unmarking all checkboxes...")
    page.unmark_all()
    assert page.are_all_unmarked(), "Not all checkboxes were unmarked"
    logger.info("All checkboxes unmarked successfully")
