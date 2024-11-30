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
    time.sleep(1)
    emailField = waitForVisibility(driver, By.ID, "input-email")  # Wait for the email input field to be visible
    emailField.send_keys("leduyquan2574@gmail.com")  # Enter the email address
    
    passwordField = waitForVisibility(driver, By.ID, "input-password")  # Wait for the password input field to be visible
    passwordField.send_keys("Quan19112003")  # Enter the password
    
    loginButton = waitForElement(driver, By.CSS_SELECTOR, "button.btn.btn-primary")  # Wait for the login button to be clickable
    loginButton.click()  # Click the login button
    
    # Wait for successful login page load (check if the title contains "My Account")
    WebDriverWait(driver, 5).until(EC.title_contains("My Account"))

def addToWishlistNologin(driver):
    """Add a product to the wishlist, with or without login."""
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40&search=iphone")  # Open the product page
    time.sleep(2)  # Wait for the page to load
    
    # Wait for the 'Add to Wishlist' button to be clickable
    wishListButton = waitForElement(driver, By.CSS_SELECTOR, "button.btn.btn-light[data-bs-toggle='tooltip']")  
    wishListButton.click()  # Click the 'Add to Wishlist' button
    time.sleep(5)  # Wait for the action to complete

    # Wait for the success message to be visible
    alertMessage = waitForVisibility(driver, By.CSS_SELECTOR, "div.alert-success")  
    assert "You must login" in alertMessage.text, "Expected login message not found."  # Assert that the login message is present
    # Compare the product name and price between the product page and wishlist

def addToWishlistLogin(driver):
    """Add a product to the wishlist, with or without login."""
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40&search=iphone")  # Open the product page
    time.sleep(2)  # Wait for the page to load
    
    # Get the product name and price from the product page
    name_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[2]/h1')))
    name_element_text = name_element.text
    price_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul[2]/li[1]/h2/span')))
    price_element_text = price_element.text

    # Wait for the 'Add to Wishlist' button to be clickable
    wishListButton = waitForElement(driver, By.CSS_SELECTOR, "button.btn.btn-light[data-bs-toggle='tooltip']")  
    wishListButton.click()  # Click the 'Add to Wishlist' button
    time.sleep(8)  # Wait for the action to complete

    button_wishlist = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top"]/div/div[2]/ul/li[3]'))
    )
    button_wishlist.click()  
    

    # Get the product name and price from the wishlist
    name_wishlist = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wishlist"]/div/table/tbody/tr/td[2]/a')))
    name_wishlist_text = name_wishlist.text
    price_wishlist = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wishlist"]/div/table/tbody/tr/td[5]/div')))
    price_wishlist_text = price_wishlist.text


    assert name_element_text == name_wishlist_text, f"Product name mismatch: {name_element_text} != {name_wishlist_text}"
    assert price_element_text == price_wishlist_text, f"Product price mismatch: {price_element_text} != {price_wishlist_text}"



def testAddToWishlistNoLogin(driver):
    """Test adding a product to the wishlist without being logged in."""
    addToWishlistNologin(driver)  # Call addToWishlist with loggedIn=False

def testAddToWishlistLogin(driver):
    """Test adding a product to the wishlist with login."""
    login(driver)  # Login to the website
    addToWishlistLogin(driver)  # Call addToWishlist with loggedIn=True
