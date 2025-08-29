from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_drag_and_drop(driver_setup):
    """
    Test drag and drop functionality on the page by swapping two boxes.
    """

    # Unpack the driver and explicit wait objects from the fixture
    driver, wait = driver_setup

    # Navigate to the drag and drop demo page
    driver.get("https://the-internet.herokuapp.com/drag_and_drop")

    # Wait until the first draggable box with ID "column-a" is present in the DOM
    box_a = wait.until(EC.presence_of_element_located((By.ID, "column-a")))
    # Wait until the second draggable box with ID "column-b" is present in the DOM
    box_b = wait.until(EC.presence_of_element_located((By.ID, "column-b")))

    # Create an ActionChains object to perform advanced user interactions like drag and drop
    actions = ActionChains(driver)

    # Perform drag and drop action: drag box_a and drop it onto box_b, then execute the action
    actions.drag_and_drop(box_a, box_b).perform()

    # After drag and drop, find the header element inside box_a and get its text
    header_a = box_a.find_element(By.TAG_NAME, "header").text
    # Similarly, find the header inside box_b and get its text
    header_b = box_b.find_element(By.TAG_NAME, "header").text

    # Assert that box_a now has header text "B", meaning the boxes swapped correctly
    assert header_a == "B", f"Expected Box A header to be 'B', but got '{header_a}'"
    # Assert that box_b now has header text "A", confirming the swap
    assert header_b == "A", f"Expected Box B header to be 'A', but got '{header_b}'"
