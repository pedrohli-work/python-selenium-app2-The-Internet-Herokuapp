import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.drag_and_drop_page import DragAndDropPage
from utils.logger import get_logger

logger = get_logger("TestDragAndDrop")


@pytest.mark.drag_and_drop
def test_drag_and_drop(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: Drag and Drop Functionality

    Verifies that Box A can be dragged and dropped onto Box B and that their headers swap correctly.

    Test Steps:
    1. Open the Drag and Drop page.
    2. Perform a drag-and-drop action from Box A to Box B.
    3. Retrieve the headers of Box A and Box B.
    4. Assert that the headers have swapped correctly.

    Expected Results:
    - Box A's header should now be 'B'.
    - Box B's header should now be 'A'.
    """
    page = DragAndDropPage(driver, wait)
    logger.info("Starting drag and drop test")

    # Open the Drag and Drop page
    page.open()
    logger.debug("Drag and Drop page opened successfully")

    # ---- Perform drag and drop ----
    page.drag_and_drop_boxes()
    logger.info("Performed drag and drop action")

    # ---- Verify box headers after drag and drop ----
    header_a, header_b = page.get_box_headers()
    assert header_a == "B", f"Expected Box A header to be 'B', got '{header_a}'"
    assert header_b == "A", f"Expected Box B header to be 'A', got '{header_b}'"
    logger.info("Box headers verified successfully after drag and drop")

    logger.info("Drag and drop test completed successfully")
