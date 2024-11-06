import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

@pytest.fixture
def driver():
    """Fixture to initialize the WebDriver."""
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    yield driver  # Yield the driver to the test
    driver.quit()  # Quit the WebDriver after the test

def goToProductPage(driver, url):
    """Navigate to the product page."""
    driver.get(url)  # Open the provided product URL
    time.sleep(2)  # Wait for the page to load

def addToCart(driver):
    """Add the product to the cart."""
    wait = WebDriverWait(driver, 2)  # Wait up to 2 seconds for elements to be clickable
    addToCartButton = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))  # Wait until the 'Add to Cart' button is clickable
    addToCartButton.click()  # Click the 'Add to Cart' button
    time.sleep(2)  # Wait for the action to complete

def goToCheckoutPage(driver):
    """Navigate to the checkout page."""
    driver.get("http://localhost/webopencart/index.php?route=checkout/cart&language=en-gb")  # Open the checkout cart URL
    time.sleep(2)  # Wait for the page to load

def proceedToCheckout(driver):
    """Click the checkout button to proceed to the next page."""
    wait = WebDriverWait(driver, 2)  # Wait up to 2 seconds for elements to be clickable
    checkoutButton = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))  # Wait until the 'Checkout' link is clickable
    checkoutButton.click()  # Click the 'Checkout' button
    time.sleep(2)  # Wait for the action to complete

def selectGuestCheckout(driver):
    """Select the 'Guest' checkout option."""
    inputGuest = WebDriverWait(driver, 2).until(  # Wait until the 'Guest' option is clickable
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#input-guest"))
    )
    inputGuest.click()  # Click the 'Guest' checkout option
    time.sleep(2)  # Wait for the action to complete

def fillShippingInformation(driver, firstName, lastName, email, company, address1, address2, city, postCode, country, region):
    """Fill in the shipping information for checkout."""
    driver.find_element(By.CSS_SELECTOR, "#input-firstname").send_keys(firstName)  # Fill in first name
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-lastname").send_keys(lastName)  # Fill in last name
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-email").send_keys(email)  # Fill in email address
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-company").send_keys(company)  # Fill in company name
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-1").send_keys(address1)  # Fill in the first address line
    time.sleep(2)  # Wait for the input to register
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-2"))  # Scroll to the second address line
    time.sleep(2)  # Wait for the page to load
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-2").send_keys(address2)  # Fill in the second address line
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-city").send_keys(city)  # Fill in the city
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-postcode").clear()  # Clear any existing postcode
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-postcode").send_keys(postCode)  # Fill in the postcode
    time.sleep(2)  # Wait for the input to register
    Select(driver.find_element(By.CSS_SELECTOR, "#input-shipping-country")).select_by_visible_text(country)  # Select the country from the dropdown
    time.sleep(2)  # Wait for the dropdown to register
    Select(driver.find_element(By.CSS_SELECTOR, "#input-shipping-zone")).select_by_visible_text(region)  # Select the region from the dropdown
    driver.find_element(By.CSS_SELECTOR, "#button-register").click()  # Click the 'Register' button
    time.sleep(5)  # Wait for the action to complete
    driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-2"))  # Scroll to the bottom of the page
    time.sleep(4)  # Wait for the page to load

def proceedWithShippingMethod(driver):
    """Choose the shipping method and proceed."""
    driver.find_element(By.CSS_SELECTOR, "#button-shipping-methods").click()  # Click the 'Shipping Methods' button
    time.sleep(2)  # Wait for the page to load
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-method-flat-flat").click()  # Select the shipping method
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#button-shipping-method").click()  # Click the 'Proceed' button
    time.sleep(2)  # Wait for the action to complete

def selectPaymentMethod(driver):
    """Select the payment method and proceed."""
    driver.find_element(By.CSS_SELECTOR, "#button-payment-methods").click()  # Click the 'Payment Methods' button
    time.sleep(2)  # Wait for the page to load
    driver.find_element(By.CSS_SELECTOR, "#input-payment-method-cod-cod").click()  # Select the 'Cash on Delivery' payment option
    time.sleep(2)  # Wait for the input to register
    driver.find_element(By.CSS_SELECTOR, "#button-payment-method").click()  # Click the 'Proceed' button
    time.sleep(2)  # Wait for the action to complete
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-2"))  # Scroll to the bottom of the page
    time.sleep(5)  # Wait for the page to load

def confirmOrder(driver):
    """Confirm the order and verify the success message."""
    driver.find_element(By.CSS_SELECTOR, "#button-confirm").click()  # Click the 'Confirm' button
    time.sleep(5)  # Wait for the action to complete
    notification = driver.find_element(By.CSS_SELECTOR, "#content > h1")  # Locate the order confirmation notification
    notificationActual = notification.text  # Get the actual notification text
    notificationExpected = "Your order has been placed!"  # Expected notification text
    assert notificationExpected == notificationActual, "Order was not placed successfully"  # Assert that the order was placed successfully

def testCheckoutWithGuestAccount(driver):
    """Test for placing an order as a guest."""
    goToProductPage(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch")  # Go to the product page
    addToCart(driver)  # Add the product to the cart
    goToCheckoutPage(driver)  # Go to the checkout page
    proceedToCheckout(driver)  # Proceed to the checkout page
    selectGuestCheckout(driver)  # Select guest checkout
    
    # Fill in shipping information
    fillShippingInformation(driver, "Lê", "Quân", "leduyquan2574@gmail.com", "Jung Talents", 
                              "264/50 Lê Văn Quới", "drgrdfgdf", "Ho Chi Minh City", "191103", "Viet Nam", "Ho Chi Minh City")
    
    proceedWithShippingMethod(driver)  # Proceed with the shipping method
    selectPaymentMethod(driver)  # Select the payment method
    confirmOrder(driver)  # Confirm the order

def testGuestAccountEmptyRequiredInput(driver):
    """Test the scenario where required fields are missing for guest checkout."""
    goToProductPage(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch")  # Go to the product page
    addToCart(driver)  # Add the product to the cart
    goToCheckoutPage(driver)  # Go to the checkout page
    proceedToCheckout(driver)  # Proceed to the checkout page
    selectGuestCheckout(driver)  # Select guest checkout
    
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "#button-register"))  # Scroll to the second address line
    time.sleep(2)  # Wait for the page to load
    # Try to proceed without filling the required fields
    driver.find_element(By.CSS_SELECTOR, "#button-register").click()  # Click the 'Register' button
    time.sleep(2)  # Wait for the page to load
    driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_element(By.CSS_SELECTOR, "#checkout-shipping-method"))  # Scroll to the second address line
    time.sleep(2)  # Wait for the page to load
    error_message_element = driver.find_element(By.ID, "error-firstname")
    error_message_text = error_message_element.text
    notificationExpected = "First Name must be between 1 and 32 characters!"  # Expected error text
    assert notificationExpected == error_message_text, "Error: Required fields were not validated"

