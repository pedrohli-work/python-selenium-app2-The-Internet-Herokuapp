from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_dynamic_controls(driver_setup):
    """
    Test dynamic controls page:
    - Remove and add checkbox
    - Enable, type in, and disable input field
    Validates each step via explicit waits and asserts.
    """

    # Unpack the driver and explicit wait from the fixture
    driver, wait = driver_setup

    # Navigate to the dynamic controls demo page
    driver.get("https://the-internet.herokuapp.com/dynamic_controls")

    # Wait for the "Remove" button to be clickable and then click it to remove the checkbox
    remove_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Remove']")))
    remove_button.click()

    # Wait until the checkbox element is no longer visible in the DOM
    wait.until(EC.invisibility_of_element_located((By.ID, "checkbox")))
    
    # Find all elements with ID "checkbox" to check if it was removed
    checkboxes = driver.find_elements(By.ID, "checkbox")

    # Assert that no checkbox elements remain (length should be zero)
    assert len(checkboxes) == 0, "Checkbox was not removed."

    # Wait for the "Add" button to be clickable and click it to add the checkbox back
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add']")))
    add_button.click()

    # Wait until the checkbox element is present in the DOM again
    checkbox = wait.until(EC.presence_of_element_located((By.ID, "checkbox")))

    # Assert that the checkbox is displayed on the page
    assert checkbox.is_displayed(), "Checkbox was not added back."

    # Find the "Enable" button and click it to enable the input field
    enable_button = driver.find_element(By.XPATH, "//button[text()='Enable']")
    enable_button.click()

    # Wait until the input field becomes clickable (enabled)
    input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
    
    # Type text into the now-enabled input field
    input_field.send_keys("Testing dynamic controls")
    
    # Assert the input field is enabled (disabled attribute should be None)
    assert input_field.get_attribute("disabled") is None, "Input field is not enabled."

    # Find the "Disable" button and click it to disable the input field
    disable_button = driver.find_element(By.XPATH, "//button[text()='Disable']")
    disable_button.click()

    # Wait until the input field has the "disabled" attribute set
    wait.until(EC.element_attribute_to_include((By.CSS_SELECTOR, "input[type='text']"), "disabled"))
    
    # Assert the input field is disabled (disabled attribute equals "true" or "disabled")
    assert input_field.get_attribute("disabled") == "true" or input_field.get_attribute("disabled") == "disabled", "Input field is not disabled."