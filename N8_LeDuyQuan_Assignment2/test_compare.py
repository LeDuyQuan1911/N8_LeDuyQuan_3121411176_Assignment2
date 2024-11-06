from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pytest
import time
from selenium.webdriver.firefox.options import Options

@pytest.fixture
def driver():
    """Initialize the WebDriver."""
    driver = webdriver.Chrome()  # Initialize Chrome WebDriver
    yield driver  # Yield the driver to the test
    driver.quit()  # Quit the WebDriver after the test

def testCompareProducts(driver):
    """Test to compare two products and check if they are added to the comparison list."""

    # Open the product page for the first product
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=30")
    time.sleep(2)  # Wait for the page to load

    # Get the product name from the page (h1 element)
    productNamePage1 = driver.find_element(By.TAG_NAME, 'h1').text

    # Find and click the 'Add to Compare' button for the first product
    iElement = driver.find_element(By.CSS_SELECTOR, 'i.fa-solid.fa-arrow-right-arrow-left')
    addToCompareButton1 = iElement.find_element(By.XPATH, '..')  # Find the parent element <button>
    addToCompareButton1.click()  # Click the button to add the product to the compare list
    time.sleep(2)  # Wait for the action to complete

    # Open the product page for the second product
    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40")
    time.sleep(2)  # Wait for the page to load

    # Get the product name from the second product page (h1 element)
    productNamePage2 = driver.find_element(By.TAG_NAME, 'h1').text

    # Find and click the 'Add to Compare' button for the second product
    iElement = driver.find_element(By.CSS_SELECTOR, 'i.fa-solid.fa-arrow-right-arrow-left')
    addToCompareButton2 = iElement.find_element(By.XPATH, '..')  # Find the parent element <button>
    addToCompareButton2.click()  # Click the button to add the product to the compare list
    time.sleep(2)  # Wait for the action to complete

    # Navigate to the comparison page
    driver.get("http://localhost/webopencart/index.php?route=product/compare&language=en-gb")
    time.sleep(2)  # Wait for the page to load

    # Get the names of products on the comparison page
    productLinks = driver.find_elements(By.XPATH, "//tr//td/a/strong")
    productNamesOnComparePage = [product.text for product in productLinks]

    # Check if the product names from the product pages are present in the comparison list
    assert productNamePage1 in productNamesOnComparePage, "The product name does not match the comparison list."
    assert productNamePage2 in productNamesOnComparePage, "The second product name does not match the comparison list."


