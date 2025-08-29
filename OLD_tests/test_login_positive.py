# Import 'By' to locate elements on the page using different strategies 
# (ID, CSS_SELECTOR, etc.)
from selenium.webdriver.common.by import By
# Import expected_conditions for explicit waits on specific element states 
# (presence, visibility, etc.)
from selenium.webdriver.support import expected_conditions as EC


def test_login_positive(driver_setup):
    """
    Test the positive login with a valid user and password.
    Verify if the success message apears correctly.
    """

    # Unpack the 'driver' (browser controller) and 
    # 'wait' (explicit wait helper) from the fixture
    driver, wait = driver_setup
    
    # Navigate the browser to the login page URL
    driver.get("https://the-internet.herokuapp.com/login")

    # Wait until the username input field is present in the DOM, then retrieve it
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    # Type the username 'tomsmith' into the username input field
    username_field.send_keys("tomsmith")

    # Find the password input field by its ID 
    # (no explicit wait here, assuming page already loaded)
    password_field = driver.find_element(By.ID, "password")
    # Type the password 'SuperSecretPassword!' into the password input field
    password_field.send_keys("SuperSecretPassword!")

    # Locate the login button using a CSS selector targeting button elements with class 'radius'
    login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
    # Click the login button to submit the form
    login_button.click()

    # Wait until the feedback message element (with ID 'flash') is visible on the page
    flash_message = wait.until(EC.visibility_of_element_located((By.ID, "flash")))

    # Assert that the success message text appears within the feedback element's text
    assert "You logged into a secure area!" in flash_message.text
