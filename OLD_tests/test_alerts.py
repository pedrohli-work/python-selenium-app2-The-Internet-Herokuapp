from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_javascript_alerts(driver_setup):
    """
    Test the handling of JavaScript alerts: simple alert, confirm (dismiss), and prompt (input).
    Verify that the expected results appear on the page after each action.
    """
    
    # Unpack the driver and explicit wait from the fixture
    driver, wait = driver_setup

    # Navigate to the page with JavaScript alert examples
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # Wait until the simple alert button is clickable, then click it
    simple_alert_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Click for JS Alert']")))
    simple_alert_button.click()
    # Switch focus to the opened alert dialog
    alert = driver.switch_to.alert
     # Assert that the alert text matches the expected simple alert message
    assert alert.text == "I am a JS Alert", "Unexpected simple alert text"
    # Accept (click OK) on the simple alert
    alert.accept()

    # Locate the confirm alert button and click it
    confirm_alert_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']")
    confirm_alert_button.click()
    # Switch focus to the confirm alert dialog
    alert = driver.switch_to.alert
    # Assert the confirm alert text is as expected
    assert alert.text == "I am a JS Confirm", "Unexpected confirm alert text"
    # Dismiss (click Cancel) the confirm alert
    alert.dismiss()

    # Locate the prompt alert button and click it
    prompt_alert_button = driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']")
    prompt_alert_button.click()
    # Switch focus to the prompt alert dialog
    alert = driver.switch_to.alert
    # Assert the prompt alert text is correct
    assert alert.text == "I am a JS prompt", "Unexpected prompt alert text"
    # Send input text to the prompt alert
    alert.send_keys("Pedro was here!")
    # Accept (click OK) the prompt alert
    alert.accept()

    # Wait until the result message appears on the page
    result = wait.until(EC.presence_of_element_located((By.ID, "result")))
    # Assert that the page shows the prompt input was registered correctly
    assert "You entered: Pedro was here!" in result.text, "Prompt input was not registered correctly"