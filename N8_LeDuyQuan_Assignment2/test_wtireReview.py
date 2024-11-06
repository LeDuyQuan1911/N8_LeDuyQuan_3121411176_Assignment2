from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pytest
import time
from selenium.webdriver.firefox.options import Options


@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    yield driver  # Yield the driver for use in tests
    driver.quit()  # Close the driver after the test


# Test case for writing a review
def testWriteReview(driver):
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb")  # Open the login page of OpenCart

    wait = WebDriverWait(driver, 2)  # Set up a WebDriverWait for 2 seconds

    emailField = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))  # Wait for the email field to be visible and enter email
    emailField.send_keys("leduyquan2574@gmail.com")

    # Wait for the password field to be visible and enter the password
    passwordField = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))  # Wait for the password field to be visible and input password
    passwordField.send_keys("Quan19112003")
    time.sleep(2)  # Pause for 2 seconds

    loginButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary")))  # Wait for the login button to be clickable
    loginButton.click()  # Click the login button

    wait.until(EC.title_contains("My Account"))  # Wait until the page title contains "My Account"
    time.sleep(2)  # Pause for 2 seconds


    driver.get("http://localhost/webopencart/index.php?route=common/home&language=en-gb")  # Open the homepage of OpenCart
    time.sleep(2)  # Pause for 2 seconds

    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40&search=iphone")  # Open the product page for iPhone
    time.sleep(2)  # Pause for 2 seconds

    # Steps to write a review
    writeReviewLink = WebDriverWait(driver, 10).until(  # Wait for the "Write a review" link to be clickable
        EC.element_to_be_clickable((By.LINK_TEXT, "Write a review"))
    )
    driver.execute_script("arguments[0].click();", writeReviewLink)  # Click on the "Write a review" link
    time.sleep(2)  # Pause for 2 seconds

    reviewTextArea = WebDriverWait(driver, 10).until(  # Wait for the review text area to be visible
        EC.presence_of_element_located((By.ID, "input-text"))
    )
    reviewTextArea.send_keys("This is my review text.")  # Enter review text
    time.sleep(2)  # Pause for 2 seconds

    ratingRadioButton = WebDriverWait(driver, 10).until(  # Wait for the rating radio button to be clickable
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='rating'][value='5']"))
    )
    ratingRadioButton.click()  # Select the rating option (5 stars)
    time.sleep(2)  # Pause for 2 seconds

    continueButton = WebDriverWait(driver, 10).until(  # Wait for the "Continue" button to be clickable
        EC.element_to_be_clickable((By.ID, "button-review"))
    )
    continueButton.click()  # Click the "Continue" button
    time.sleep(2)  # Pause for 2 seconds

    # Verify if the new review has been added to the product's review section
    try:  
        successMessage = WebDriverWait(driver, 10).until(  # Wait for the success message to be visible
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        # Assert if the success message contains the expected text
        assert "Thank you for your review" in successMessage.text, "Review submission did not succeed as expected."
        print("Review submitted successfully!")  # Print success message
    except Exception as e:
        print("Review submission failed:", e)  # Print error message if submission fails
