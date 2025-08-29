from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_iframe_text_editing(driver_setup):
    """
    Test editing content inside an iframe on the page.
    Clears the content and inserts a test string via JavaScript, then verifies it.
    """

    # Unpack the driver and explicit wait from the fixture
    driver, wait = driver_setup

    # Navigate to the frames test page
    driver.get("https://the-internet.herokuapp.com/frames")

    # Wait until the link with text "iFrame" is clickable, 
    # then click it to open the iframe example
    iframe_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "iFrame")))
    iframe_link.click()

    # Switch Selenium's focus to the iframe identified by id "mce_0_ifr"
    driver.switch_to.frame("mce_0_ifr")

    # Wait until the editable body inside the iframe 
    # (with CSS selector body#tinymce) is present in the DOM
    editable_body = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce")))

    # Use JavaScript to clear any existing HTML content inside the editable iframe body element
    driver.execute_script("arguments[0].innerHTML = '';", editable_body)

    # Define the new test text string to insert
    test_text = "Hello, this is a test!"

    # Use JavaScript to insert the test text as innerHTML of the iframe's editable body
    driver.execute_script("arguments[0].innerHTML = arguments[1];", editable_body, test_text)

    # Retrieve the actual innerText from the iframe's editable body to verify insertion
    actual_text = driver.execute_script("return arguments[0].innerText;", editable_body)

    # Assert the actual text matches the test text, fail if mismatch
    assert actual_text == test_text, "Text input inside iframe failed!"

    # Switch Selenium's focus back to the main page context from the iframe
    driver.switch_to.default_content()