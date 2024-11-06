from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium import webdriver
import pytest
from selenium.webdriver.firefox.options import Options


@pytest.fixture
def driver():
    """Fixture to initialize the WebDriver."""
    driver = webdriver.Chrome()  # Initialize Chrome WebDriver
    yield driver  # Yield the driver to the test
    driver.quit()  # Quit the WebDriver after the test

def waitForElement(driver, by, value, timeout=5):
    """Wait for an element to be clickable and return it."""
    wait = WebDriverWait(driver, timeout)  # Create a WebDriverWait instance with the specified timeout
    return wait.until(EC.element_to_be_clickable((by, value)))  # Wait until the element is clickable and return it

def waitForVisibility(driver, by, value, timeout=5):
    """Wait for an element to be visible and return it."""
    wait = WebDriverWait(driver, timeout)  # Create a WebDriverWait instance with the specified timeout
    return wait.until(EC.visibility_of_element_located((by, value)))  # Wait until the element is visible and return it

def login(driver):
    """Login to OpenCart."""
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb")  # Open the login page
    emailField = waitForVisibility(driver, By.ID, "input-email")  # Wait for the email input field to be visible
    emailField.send_keys("leduyquan2574@gmail.com")  # Enter the email address
    
    passwordField = waitForVisibility(driver, By.ID, "input-password")  # Wait for the password input field to be visible
    passwordField.send_keys("Quan19112003")  # Enter the password
    
    loginButton = waitForElement(driver, By.CSS_SELECTOR, "button.btn.btn-primary")  # Wait for the login button to be clickable
    loginButton.click()  # Click the login button
    
    # Wait for successful login page load (check if the title contains "My Account")
    WebDriverWait(driver, 5).until(EC.title_contains("My Account"))

def addToWishlist(driver, loggedIn=False):
    """Add a product to the wishlist, with or without login."""
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40&search=iphone")  # Open the product page
    time.sleep(2)  # Wait for the page to load
    wishListButton = waitForElement(driver, By.CSS_SELECTOR, "button.btn.btn-light[data-bs-toggle='tooltip']")  # Wait for the 'Add to Wishlist' button to be clickable
    wishListButton.click()  # Click the 'Add to Wishlist' button
    time.sleep(5)  # Wait for the action to complete
    
    alertMessage = waitForVisibility(driver, By.CSS_SELECTOR, "div.alert-success")  # Wait for the success message to be visible
    if loggedIn:  # Check if the user is logged in
        assert "You must login" not in alertMessage.text, "Unexpected message found after login."  # Assert that the login message does not appear
    else:  # If not logged in
        assert "You must login" in alertMessage.text, "Expected login message not found."  # Assert that the login message is present

def testAddToWishlistNoLogin(driver):
    """Test adding a product to the wishlist without being logged in."""
    addToWishlist(driver, loggedIn=False)  # Call addToWishlist with loggedIn=False

def testAddToWishlistLogin(driver):
    """Test adding a product to the wishlist with login."""
    login(driver)  # Login to the website
    addToWishlist(driver, loggedIn=True)  # Call addToWishlist with loggedIn=True
