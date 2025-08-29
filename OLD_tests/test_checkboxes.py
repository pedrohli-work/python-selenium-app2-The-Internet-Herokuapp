from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_checkboxes(driver_setup):
    """
    Test toggling all checkboxes on the page: mark all unchecked and then unmark all checked.
    Verifies the final state after each step with assertions.
    """

    driver, wait = driver_setup

    # Open the target page with checkboxes
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    
    # Wait until all checkboxes are located in the DOM
    checkboxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']")))

    # Mark all checkboxes that are unchecked
    for checkbox in checkboxes:
        # If checkbox is not selected, select it
        if not checkbox.is_selected():
            checkbox.click()
    assert all(cb.is_selected() for cb in checkboxes), "Not all checkboxes were checked."
       
    # Unmark all checkboxes that are checked
    for checkbox in checkboxes:
        checkbox.click()
    assert all(not cb.is_selected() for cb in checkboxes), "Not all checkboxes were unchecked."
