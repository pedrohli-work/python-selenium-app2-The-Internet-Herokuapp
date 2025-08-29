from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_inputs(driver_setup):
    """
    Tests input field accepting numbers and rejects non-numeric input.
    """

    driver, wait = driver_setup
    
    # Navigates to the URL of the inputs page that will be tested.
    driver.get("https://the-internet.herokuapp.com/inputs")

    # Wait until the input field is present on the page
    input_field = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    # Clear any existing text in the input field
    input_field.clear()

    # Type a number into the input field
    input_field.send_keys("12345")

    # Clear the field again
    input_field.clear()

    # Type a negative number into the input field
    input_field.send_keys("-678")

    # Type some non-numeric input (the field should ignore or reject it)
    input_field.send_keys("abc")
    input_field.clear()

    # Iterates over each character in the string "42".
    for key in "42":
        # Sends each individual character to the input field.
        input_field.send_keys(key)