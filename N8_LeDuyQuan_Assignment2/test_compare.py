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
    driver = webdriver.Chrome()  
    yield driver  
    driver.quit()  

def testCompareProducts(driver):
    """Test to compare two products and check if they are added to the comparison list."""

    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=30")
    time.sleep(2)  

    productNamePage1 = driver.find_element(By.TAG_NAME, 'h1').text

    iElement = driver.find_element(By.CSS_SELECTOR, 'i.fa-solid.fa-arrow-right-arrow-left')
    addToCompareButton1 = iElement.find_element(By.XPATH, '..')  
    addToCompareButton1.click()  
    time.sleep(2) 

    driver.get("http://localhost/webopencart/index.php?route=product/product&language=en-gb&product_id=40")
    time.sleep(2)  

    productNamePage2 = driver.find_element(By.TAG_NAME, 'h1').text

    iElement = driver.find_element(By.CSS_SELECTOR, 'i.fa-solid.fa-arrow-right-arrow-left')
    addToCompareButton2 = iElement.find_element(By.XPATH, '..') 
    addToCompareButton2.click()
    time.sleep(2)  

    driver.get("http://localhost/webopencart/index.php?route=product/compare&language=en-gb")
    time.sleep(2)  

    productLinks = driver.find_elements(By.XPATH, "//tr//td/a/strong")
    productNamesOnComparePage = [product.text for product in productLinks]

    assert productNamePage1 in productNamesOnComparePage, "The product name does not match the comparison list."
    assert productNamePage2 in productNamesOnComparePage, "The second product name does not match the comparison list."


