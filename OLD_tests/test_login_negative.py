from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_login_negative(driver_setup):
    """
    Tests negative login with invalid credentials.
    Verifies that the appropriate error message is displayed.
    """
     
    driver, wait = driver_setup

    driver.get("https://the-internet.herokuapp.com/login")

    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_field.send_keys("wronguser")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("wrongpassword")

    login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
    login_button.click()

    flash_message = wait.until(EC.visibility_of_element_located((By.ID, "flash")))
    assert "Your username is invalid!" in flash_message.text or "Your password is invalid!" in flash_message.text

