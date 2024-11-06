import time
from selenium.webdriver.support.ui import Select
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Define a fixture to create and quit the driver for each test
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Initialize Chrome WebDriver
    yield driver  # Yield the driver to the test
    driver.quit()  # Quit the WebDriver after the test

# Login function to log in using email and password
def login(driver, email, password):
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb")  
    wait = WebDriverWait(driver, 2)  # Wait for elements to be present
    emailField = wait.until(EC.visibility_of_element_located((By.ID, "input-email")))  # Wait for email field to be visible
    emailField.send_keys(email)  # Enter email in the email field

    passwordField = wait.until(EC.visibility_of_element_located((By.ID, "input-password")))  # Wait for password field to be visible
    passwordField.send_keys(password)  # Enter password in the password field
    time.sleep(2)  # Wait for 2 seconds

    loginButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary")))  # Wait for login button to be clickable
    loginButton.click()  # Click the login button

    wait.until(EC.title_contains("My Account"))  # Wait until "My Account" page is loaded

# Add a product to the cart
def addProductToCart(driver, productUrl):
    driver.get(productUrl)  # Open the product page
    wait = WebDriverWait(driver, 2)  # Wait for elements to be present
    addToCartButton = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))  # Wait for 'Add to Cart' button to be clickable
    addToCartButton.click()  # Click the 'Add to Cart' button
    time.sleep(2)  # Wait for 2 seconds

# Proceed to checkout page
def proceedToCheckout(driver):
    driver.get("http://localhost/webopencart/index.php?route=checkout/cart&language=en-gb")  # Open the checkout page
    wait = WebDriverWait(driver, 2)  # Wait for elements to be present
    checkoutButton = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Checkout")))  # Wait for checkout button to be clickable
    checkoutButton.click()  # Click the checkout button
    time.sleep(2)  # Wait for 2 seconds

# Select shipping address
def selectShippingAddress(driver, address):
    wait = WebDriverWait(driver, 2)  # Wait for elements to be present
    shippingAddressDropdown = wait.until(EC.element_to_be_clickable((By.ID, "input-shipping-address")))  # Wait for shipping address dropdown to be clickable
    select = Select(shippingAddressDropdown)  # Create a Select object
    select.select_by_visible_text(address)  # Select the address from the dropdown
    time.sleep(2)  # Wait for 2 seconds

# Select shipping method
def selectShippingMethod(driver):
    driver.execute_script("arguments[0].scrollIntoView(false);", driver.find_element(By.CSS_SELECTOR, "#button-shipping-methods"))
    time.sleep(4)
    wait = WebDriverWait(driver, 2)  # Wait for elements to be present
    shippingMethod = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#button-shipping-methods")))  # Wait for shipping method button to be clickable
    shippingMethod.click()  # Click the shipping method button
    time.sleep(2)  # Wait for 2 seconds

    methodFlat = driver.find_element(By.CSS_SELECTOR, "#input-shipping-method-flat-flat")  # Find the flat shipping method
    methodFlat.click()  # Select the flat shipping method
    time.sleep(2)  # Wait for 2 seconds

    continueButton = driver.find_element(By.CSS_SELECTOR, "#button-shipping-method")  # Find the continue button
    continueButton.click()  # Click the continue button
    time.sleep(2)  # Wait for 2 seconds

# Select payment method
def selectPaymentMethod(driver):
    paymentMethod = driver.find_element(By.CSS_SELECTOR, "#button-payment-methods")  # Find the payment method button
    paymentMethod.click()  # Click the payment method button
    time.sleep(2)  # Wait for 2 seconds

    cashMethod = driver.find_element(By.CSS_SELECTOR, "#input-payment-method-cod-cod")  # Find the cash on delivery method
    cashMethod.click()  # Select cash on delivery payment method
    time.sleep(2)  # Wait for 2 seconds

    continueButton = driver.find_element(By.CSS_SELECTOR, "#button-payment-method")  # Find the continue button for payment method
    continueButton.click()  # Click the continue button
    time.sleep(2)  # Wait for 2 seconds

    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "#button-confirm"))  # Scroll to the confirm button
    time.sleep(5)  # Wait for 5 seconds

# Confirm the order
def confirmOrder(driver):
    confirmOrderButton = driver.find_element(By.CSS_SELECTOR, "#button-confirm")  # Find the confirm order button
    confirmOrderButton.click()  # Click the confirm order button
    time.sleep(2)  # Wait for 2 seconds

# Check the order confirmation
def checkOrderConfirmation(driver):
    notification = driver.find_element(By.CSS_SELECTOR, "#content > h1")  # Find the order confirmation notification
    notificationActual = notification.text  # Get the actual notification text
    notificationExpected = "Your order has been placed!"  # The expected notification text
    assert notificationExpected == notificationActual, "Order not successfully placed"  # Assert that the order confirmation matches the expected text

# Test case for checkout with existing address
def testCheckoutWithExistAddress(driver):
    login(driver, "leduyquan2574@gmail.com", "Quan19112003")  # Log in with email and password
    addProductToCart(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch")  # Add product to cart
    proceedToCheckout(driver)  # Proceed to checkout
    selectShippingAddress(driver, "iyui iyui, ityuiyu, iyuiytui, Alo, Wallis and Futuna Islands")  # Select shipping address
    selectShippingMethod(driver)  # Select shipping method
    selectPaymentMethod(driver)  # Select payment method
    confirmOrder(driver)  # Confirm the order
    checkOrderConfirmation(driver)  # Check if the order is confirmed

# Test case for checkout with new address
def testCheckoutWithNewAddress(driver):
    login(driver, "leduyquan2574@gmail.com", "Quan19112003")  # Log in with email and password
    addProductToCart(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch")  # Add product to cart
    proceedToCheckout(driver)  # Proceed to checkout

    # Fill in a new shipping address
    shippingCheckbox = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "input-shipping-new")))  # Wait for the new address checkbox
    if not shippingCheckbox.is_selected():  # Check if the checkbox is not selected
        shippingCheckbox.click()  # Select the checkbox
    time.sleep(5)  # Wait for 5 seconds

    # Fill in the new shipping address details
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-firstname").send_keys("Lê")  # Enter first name
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-lastname").send_keys("Quân")  # Enter last name
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-company").send_keys("Jung Talents")  # Enter company name
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-1").send_keys("264/50 Lê Văn Quới")  # Enter address line 1
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-2"))  # Scroll to the next address field
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-address-2").send_keys("drgrdfgdf")  # Enter address line 2
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-city").send_keys("Ho Chi Minh City")  # Enter city
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-postcode").clear()  # Clear the postcode field
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#input-shipping-postcode").send_keys("191103")  # Enter postcode
    time.sleep(2)
    Select(driver.find_element(By.CSS_SELECTOR, "#input-shipping-country")).select_by_visible_text("Viet Nam")  # Select the country
    time.sleep(2)
    Select(driver.find_element(By.CSS_SELECTOR, "#input-shipping-zone")).select_by_visible_text("Bac Giang")  # Select the region
    time.sleep(2)
    continue_btn = driver.find_element(By.CSS_SELECTOR, "#button-shipping-address")
    continue_btn.click()
    time.sleep(2)

    selectShippingMethod(driver)  # Select shipping method
    selectPaymentMethod(driver)  # Select payment method
    confirmOrder(driver)  # Confirm the order
    checkOrderConfirmation(driver)  # Check if the order is confirmed
