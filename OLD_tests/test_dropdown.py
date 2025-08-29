from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def test_dropdown(driver_setup):
    """
    Test the dropdown element by selecting options via visible text and value,
    verifying the selection after each action.
    """

    driver, wait = driver_setup

    # Navigate to the dropdown test page
    driver.get("https://the-internet.herokuapp.com/dropdown")

    # Wait for the dropdown element to be present in the DOM
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "dropdown")))

    # Create a Select object to interact with dropdown options
    dropdown = Select(dropdown_element)

    # Select "Option 1" by visible text and verify
    # Finds the dropdown option with the visible label "Option 1" and selects it
    dropdown.select_by_visible_text("Option 1")
    # Retrieves the text of the currently selected option
    selected_option = dropdown.first_selected_option.text
    # Checks if the selected option text matches "Option 1"
    assert selected_option == "Option 1", "Failed to select Option 1"

    # Select "Option 2" by value and verify
    # Finds and selects the option where the HTML 'value' attribute equals "2"
    dropdown.select_by_value("2")
    # Retrieves the text of the currently selected option again
    selected_option = dropdown.first_selected_option.text
    # Verifies the selected option text matches "Option 2"
    assert selected_option == "Option 2", "Failed to select Option 2"