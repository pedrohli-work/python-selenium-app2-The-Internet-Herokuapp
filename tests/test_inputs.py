import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.inputs_page import InputsPage
from utils.logger import get_logger

# Dedicated logger for input field tests
logger = get_logger("TestInputs")


@pytest.mark.inputs
def test_inputs(driver: WebDriver, wait: WebDriverWait) -> None:
    """
    Test Case: Inputs Page Functionality

    Verifies the behavior of the numeric input field on the Inputs page.

    Test Scenarios:
    1. Typing a positive number → value should be accepted.
    2. Typing a negative number → value should be accepted.
    3. Typing letters → input should ignore them and remain empty.
    4. Typing digits one by one → final concatenated number should match.

    Expected Results:
    - Only numeric values (positive or negative) should persist in the field.
    - Non-numeric input (letters) should be ignored.
    - Sequential typing of digits should work as expected.
    """
    page = InputsPage(driver, wait)
    logger.info("Opening Inputs page")
    
    # Open the Inputs page
    page.open()
    logger.debug("Inputs page opened successfully")

    # ---- Test 1: Type a positive number ----
    page.clear_field()
    logger.info("Typing positive number: 12345")
    page.type_value("12345")
    input_value = page.get_input_field().get_attribute("value")
    assert input_value == "12345", f"Expected input value '12345', got '{input_value}'"

    # ---- Test 2: Type a negative number ----
    page.clear_field()
    logger.info("Typing negative number: -678")
    page.type_value("-678")
    input_value = page.get_input_field().get_attribute("value")
    assert input_value == "-678", f"Expected input value '-678', got '{input_value}'"

    # ---- Test 3: Try typing letters (should be ignored) ----
    page.clear_field()
    logger.info("Typing letters: abc (should be ignored)")
    page.type_value("abc")
    input_value = page.get_input_field().get_attribute("value")
    assert input_value == "", f"Expected empty input when typing letters, got '{input_value}'"

    # ---- Test 4: Type sequence of digits one by one ----
    page.clear_field()
    logger.info("Typing sequence of digits one by one: 42")
    page.type_each_char("42")
    input_value = page.get_input_field().get_attribute("value")
    assert input_value == "42", f"Expected input value '42', got '{input_value}'"

    logger.info("Inputs page test completed successfully")
