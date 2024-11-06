from selenium.webdriver.common.by import By  # Import necessary classes and methods from Selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pytest
import time
from selenium.webdriver.common.keys import Keys


# Create a 'driver' fixture for pytest
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    yield driver
    driver.quit()  # Quit the driver after the test completes


# Function to open the webpage
def openWebPage(driver, url):
    driver.get(url)  # Open the provided URL
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )  # Wait for the 'body' element to appear


# Function to set the window size
def setWindowSize(driver, width, height):
    driver.set_window_size(width, height)
    driver.refresh()  # Refresh the page to apply the new size


# Function to check if elements are displayed
def checkElementVisibility(driver, element, device, elementName):
    assert element.is_displayed(), f"{elementName} is not displayed on {device}."


# Function to search for a product
def searchProduct(driver, productName):
    searchBox = driver.find_element(By.NAME, "search")
    searchBox.clear()
    searchBox.send_keys(productName + Keys.RETURN)


# Function to add a product to the cart
def addProductToCart(driver):
    addToCartButton = driver.find_element(By.CSS_SELECTOR, "button[type='submit'][data-bs-toggle='tooltip']")
    addToCartButton.click()


# Function to navigate to the shopping cart
def goToShoppingCart(driver):
    shoppingCartLink = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='Shopping Cart']"))
    )
    shoppingCartLink.click()


# Function to check if products are in the cart
def checkProductsInCart(driver):
    checkoutCartDiv = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "checkout-cart"))
    )
    productsInCart = checkoutCartDiv.find_elements(By.CLASS_NAME, "product-thumb")
    assert len(productsInCart) > 0, "No products found in the cart."
    assert checkoutCartDiv.is_displayed(), "Checkout cart div is not displayed."
    print("Checkout cart div is displayed successfully.")


# Main function to test responsive design
def testResponsiveDesign(driver):
    url = "http://localhost/webopencart/index.php?route=common/home&language=en-gb"
    driver.get(url)  # Open the homepage of the OpenCart demo site

    # Define the viewport sizes for Desktop, Tablet, and Mobile
    viewports = {
        "Desktop": (1200, 800),
        "Tablet": (768, 1024),
        "Mobile": (375, 667)
    }

    # Loop through each viewport size to check the interface at different sizes
    for device, (width, height) in viewports.items():
        setWindowSize(driver, width, height)  # Set the window size of the browser
        openWebPage(driver, url)  # Open the webpage and wait for body element

        try:
            # Check if search box is displayed
            searchBox = driver.find_element(By.NAME, "search")
            checkElementVisibility(driver, searchBox, device, "Search box")

            # Check if 'My Account' dropdown is displayed
            myAccountDropdown = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']")
            checkElementVisibility(driver, myAccountDropdown, device, "My Account dropdown")

            # Check if main content is displayed
            mainContent = driver.find_element(By.ID, "content")
            checkElementVisibility(driver, mainContent, device, "Main content")

            # Search for 'Iphone'
            searchProduct(driver, "Iphone")

            # Add the product to the cart
            addProductToCart(driver)

            # Go to the shopping cart
            goToShoppingCart(driver)

            # Check if the products are in the cart
            checkProductsInCart(driver)

        except Exception as e:
            print(f"Responsive test failed for {device}: {e}")

    print("Responsive design test completed.")
