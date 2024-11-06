import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
import time

# Fixture to initialize the WebDriver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Function to wait for an element to be clickable
def waitForClickableElement(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

# Function to click an element with JS execution for smooth interaction
def clickElement(driver, element):
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)

# Function to scroll to an element
def scrollToElement(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

# Function to get product names from cart
def getCartProductNames(driver):
    # Find all the product names by selecting the <a> tags inside <td> elements with the 'text-start' class
    productNames = driver.find_elements(By.CSS_SELECTOR, "#header-cart .dropdown-menu .table-striped tbody tr td.text-start a")
    
    # Extract and return the names as a list
    return [name.text.strip() for name in productNames]

# Function to get product quantities from cart
def getCartProductQuantities(driver):
    # Locate all the <td> elements that contain the quantities (in the 3rd column of the table rows)
    productQuantities = driver.find_elements(By.CSS_SELECTOR, "#header-cart .dropdown-menu .table-striped tbody tr td.text-end:nth-child(3)")
    
    quantities = []
    
    for quantity in productQuantities:
        # Get the text and remove the 'x' and any extra spaces
        quantityText = quantity.text.replace("x", "").strip()
        
        # Convert the quantity text to an integer (if it's not empty or invalid)
        quantities.append(int(quantityText) if quantityText.isdigit() else 0)

    print(quantities)
    return quantities

# Test case for adding a product to the cart
def testAddToCart(driver):
    driver.get("http://localhost/webopencart/index.php?route=common/home&language=en-gb")
    wait = WebDriverWait(driver, 2)
    
    try:
        addToCartButton = waitForClickableElement(driver, (By.CSS_SELECTOR, "#content > div.row.row-cols-1.row-cols-sm-2.row-cols-md-3.row-cols-xl-4 > div:nth-child(2) > div > div.content > form > div > button:nth-child(1)"))
        scrollToElement(driver, addToCartButton)
        clickElement(driver, addToCartButton)
        
        successMessage = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        assert "iPhone" in successMessage.text, "Product name not found in success message."
    except (TimeoutException, ElementClickInterceptedException):
        print("Retrying after refreshing the page...")
        driver.refresh()
        addToCartButton = waitForClickableElement(driver, (By.CSS_SELECTOR, "#content > div.row.row-cols-1.row-cols-sm-2.row-cols-md-3.row-cols-xl-4 > div:nth-child(2) > div > div.content > form > div > button:nth-child(1)"))
        scrollToElement(driver, addToCartButton)
        clickElement(driver, addToCartButton)
        
        successMessage = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        assert "iPhone" in successMessage.text, "Product name not found in success message after retry."

# Test case for adding a product with two quantities to the cart
def testAddProductWith2Quantity(driver):
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch")
    
    addToCartButton = waitForClickableElement(driver, (By.ID, "button-cart"))
    clickElement(driver, addToCartButton)
    time.sleep(2)
    clickElement(driver, addToCartButton)
    time.sleep(2)

    cartButton = waitForClickableElement(driver, (By.CSS_SELECTOR, "#header-cart > div > button"))
    scrollToElement(driver, cartButton)
    clickElement(driver, cartButton)
    time.sleep(2)
    
    actualProductNames = getCartProductNames(driver)
    actualQuantities = getCartProductQuantities(driver)
    
    expectedProductNames = ['HTC Touch HD']
    expectedQuantities = [2]
    
    assert sorted(expectedProductNames) == sorted(actualProductNames), "Product names do not match"
    assert expectedQuantities == actualQuantities, "Product quantities do not match"

# Test case for adding multiple products to the cart
def testAddMultipleProduct(driver):
    driver.get("http://localhost/webopencart/index.php?route=common/home&language=en-gb")
    wait = WebDriverWait(driver, 10)
    
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40&search=iphone")
    addToCartButton = waitForClickableElement(driver, (By.ID, "button-cart"))
    clickElement(driver, addToCartButton)
    
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=43")
    addToCartButton = waitForClickableElement(driver, (By.ID, "button-cart"))
    clickElement(driver, addToCartButton)
    time.sleep(2)

    cartButton = waitForClickableElement(driver, (By.CSS_SELECTOR, "#header-cart > div > button"))
    scrollToElement(driver, cartButton)
    clickElement(driver, cartButton)
    time.sleep(5)
    
    actualProductNames = getCartProductNames(driver)
    expectedProductNames = ["iPhone", "MacBook"]
    
    assert sorted(expectedProductNames) == sorted(actualProductNames), "Product names do not match"


