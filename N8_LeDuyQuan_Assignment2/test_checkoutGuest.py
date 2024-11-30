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
    """Navigate to the product page and retrieve the product price."""
    driver.get(url)  # Open the provided product URL
    # Find the price element directly
    price_element = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul[2]/li[1]/h2/span')

    # Retrieve the text from the price element
    price_text = price_element.text
    print("Product Price:", price_text)
    return price_text

def goToMultipleProductPage(driver, url1, url2):
    """Navigate to the product page and retrieve the product prices."""
    
    driver.get(url1)
    add_to_cart_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "button-cart"))
    )
    add_to_cart_button.click()  # Click the 'Add to Cart' button
    
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )  # Assuming a success alert or cart notification appears
    
    price_element1 = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul[2]/li[1]/h2/span'))
    )
    price_text1 = price_element1.text

    # Convert the price text to a float (assuming the price is in a format like "$10.99")
    price1 = float(price_text1.replace('$', '').replace(',', ''))  # Remove any currency symbol and commas

    driver.get(url2)
    add_to_cart_button2 = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "button-cart"))
    )
    add_to_cart_button2.click()  # Click the 'Add to Cart' button
    
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    
    price_element2 = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul[2]/li[1]/h2/span'))
    )
    price_text2 = price_element2.text

    # Convert the price text to a float (assuming the price is in a format like "$20.99")
    price2 = float(price_text2.replace('$', '').replace(',', ''))  # Remove any currency symbol and commas

    print(f"Product Price 1: {price1}")
    print(f"Product Price 2: {price2}")
    
    # Return the total price as the sum of both prices
    total_price = price1 + price2
    return total_price


def goToMultipleProductPageAndChangeVolume(driver, url1, url2):
    """Navigate to the product page and retrieve the product prices."""
    driver.get(url1)
    wait = WebDriverWait(driver, 4) 
    quantity_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input-quantity"]')))
    quantity_input.clear()
    quantity_input.send_keys("2")  
    time.sleep(1)  
    add_to_cart_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "button-cart"))
    )
    add_to_cart_button.click()  # Click the 'Add to Cart' button
    
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )  # Assuming a success alert or cart notification appears
    
    price_element1 = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul[2]/li[1]/h2/span'))
    )
    price_text1 = price_element1.text

    # Convert the price text to a float (assuming the price is in a format like "$10.99")
    price1 = float(price_text1.replace('$', '').replace(',', ''))  # Remove any currency symbol and commas

    driver.get(url2)
    add_to_cart_button2 = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.ID, "button-cart"))
    )
    add_to_cart_button2.click()  # Click the 'Add to Cart' button
    
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    
    price_element2 = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul[2]/li[1]/h2/span'))
    )
    price_text2 = price_element2.text

    # Convert the price text to a float (assuming the price is in a format like "$20.99")
    price2 = float(price_text2.replace('$', '').replace(',', ''))  # Remove any currency symbol and commas

    print(f"Product Price 1: {price1*2}")
    print(f"Product Price 2: {price2}")
    
    # Return the total price as the sum of both prices
    total_price = price1*2 + price2
    return total_price


    
def addToCart(driver):
    """Add the product to the cart."""
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to be clickable
    # Wait for the 'Add to Cart' button to be clickable
    add_to_cart_button = wait.until(EC.element_to_be_clickable((By.ID, "button-cart")))
    add_to_cart_button.click()  # Click the 'Add to Cart' button
    print("Add to Cart button clicked successfully.")
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

def proceedToCheckoutWithChangeVolume(driver):
    """Nhấn vào nút thanh toán và thay đổi giá trị nhập liệu từ 1 thành 2."""
    wait = WebDriverWait(driver, 2) 
    
    # Tìm và thay đổi số lượng sản phẩm
    quantity_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="shopping-cart"]/div/table/tbody/tr[1]/td[4]/form/div/input[1]')))
    quantity_input.clear()
    quantity_input.send_keys("2")  # Thay đổi số lượng thành 2
    update_button = driver.find_element(By.XPATH, '//*[@id="shopping-cart"]/div/table/tbody/tr[1]/td[4]/form/div/button[1]')  
    update_button.click()  
    time.sleep(1)  
    
    checkoutButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[3]/div[2]/a')))  # Chờ cho đến khi liên kết 'Checkout' có thể nhấp được
    driver.execute_script("arguments[0].scrollIntoView(true);", checkoutButton)
    time.sleep(2)
    checkoutButton.click()  
    time.sleep(2)  # Chờ thao tác hoàn tất

def selectGuestCheckout(driver):
    """Select the 'Guest' checkout option."""
    inputGuest = WebDriverWait(driver, 2).until(  # Wait until the 'Guest' option is clickable
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#input-guest"))
    )
    inputGuest.click()  # Click the 'Guest' checkout option
    time.sleep(2)  # Wait for the action to complete

def fillShippingInformation(driver, firstName, lastName, email, company, address1, address2, city, postCode, country, region, price_element):
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

    price_total_element = driver.find_element(By.XPATH, '//*[@id="checkout-confirm"]/div[1]/table/tfoot/tr[4]/td[2]')
    price_total_text = price_total_element.text
    print("Checkout Price:", price_total_text)
    checkout_price = float(price_total_text.replace('$', '').replace(',', '').strip())

    # Compare product price with checkout price
    print("Product Price:", price_element)
    
    if price_element == checkout_price:
        print("The prices match!")
    else:
        print(f"The prices do not match. Product Price: {price_element}, Checkout Price: {price_total_text}")
    
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
    price_element = goToProductPage(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch")  # Go to the product page
    addToCart(driver)  # Add the product to the cart
    goToCheckoutPage(driver)  # Go to the checkout page
    proceedToCheckout(driver)  # Proceed to the checkout page
    selectGuestCheckout(driver)  # Select guest checkout
    
    # Fill in shipping information
    fillShippingInformation(driver, "Lê", "Quân", "leduyquan2574@gmail.com", "Jung Talents", 
                              "264/50 Lê Văn Quới", "drgrdfgdf", "Ho Chi Minh City", "191103", "Viet Nam", "Ho Chi Minh City", price_element)
    
    proceedWithShippingMethod(driver)  # Proceed with the shipping method
    selectPaymentMethod(driver)  # Select the payment method
    confirmOrder(driver)  # Confirm the order

def testCheckoutWithGuestAccount2(driver):
    """Test for placing an order as a guest."""
    price_element = goToMultipleProductPage(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch","http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=33&path=25_28")  # Go to the product page
    goToCheckoutPage(driver)  # Go to the checkout page
    proceedToCheckout(driver)  # Proceed to the checkout page
    selectGuestCheckout(driver)  # Select guest checkout
    
    # Fill in shipping information
    fillShippingInformation(driver, "Lê", "Quân", "leduyquan2574@gmail.com", "Jung Talents", 
                              "264/50 Lê Văn Quới", "drgrdfgdf", "Ho Chi Minh City", "191103", "Viet Nam", "Ho Chi Minh City", price_element)
    
    proceedWithShippingMethod(driver)  # Proceed with the shipping method
    selectPaymentMethod(driver)  # Select the payment method
    confirmOrder(driver)  # Confirm the order

def testCheckoutWithGuestAccount3(driver):
    """Test for placing an order as a guest."""
    price_element = goToMultipleProductPageAndChangeVolume(driver, "http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=28&search=touch","http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=33&path=25_28")  # Go to the product page
    goToCheckoutPage(driver)  # Go to the checkout page
    proceedToCheckoutWithChangeVolume(driver)  # Proceed to the checkout page
    selectGuestCheckout(driver)  # Select guest checkout
    
    # Fill in shipping information
    fillShippingInformation(driver, "Lê", "Quân", "leduyquan2574@gmail.com", "Jung Talents", 
                              "264/50 Lê Văn Quới", "drgrdfgdf", "Ho Chi Minh City", "191103", "Viet Nam", "Ho Chi Minh City", price_element)
    
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

