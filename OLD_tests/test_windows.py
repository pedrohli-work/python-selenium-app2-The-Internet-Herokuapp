from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_multiple_windows(driver_setup):
    """
    Test handling multiple browser windows:
    - Open new window
    - Switch to new window and verify content
    - Close new window and return to original window
    """

    # Unpack the driver and explicit wait from the fixture
    driver, wait = driver_setup

    # Navigate to the page with multiple windows example
    driver.get("https://the-internet.herokuapp.com/windows")

    # Store the handle (ID) of the current window (original)
    original_window = driver.current_window_handle

    # Wait until the link with text "Click Here" is clickable 
    # and click it to open a new window
    new_window_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here")))
    new_window_link.click()

    # Wait until the number of open windows is 2 (the new one opened)
    wait.until(EC.number_of_windows_to_be(2))

    # Get a list of all currently open window handles
    all_windows = driver.window_handles

    # Iterate over all windows and switch to the one that is not the original window
    for window_handle in all_windows:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    # Wait for the heading element <h3> to be present in the new window
    heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

    # Assert the heading text is exactly "New Window", else fail with message
    assert heading.text == "New Window", "Unexpected heading text in new window."

    # Close the current window (the new one)
    driver.close()

    # Switch back to the original window using its stored handle
    driver.switch_to.window(original_window)
    
    # Assert that the driver focus is back to the original window, else fail
    assert driver.current_window_handle == original_window, "Did not switch back to original window."