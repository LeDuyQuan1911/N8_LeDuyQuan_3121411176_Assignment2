import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.options import Options
import pytest


# Pytest fixture to initialize and quit the driver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    yield driver  # Yield the driver for testing
    driver.quit()  # Quit the driver after the test completes


# Function to log in with email and password
def login(driver, email, password):
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb")  # Navigate to login page
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "input-email"))).send_keys(email)  # Wait for email field and input email
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "input-password"))).send_keys(password)  # Wait for password field and input password
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()  # Click the submit button
    time.sleep(2)  # Wait for login to complete


# Function to check if the search box is present
def searchBoxPresent(driver):
    return WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.NAME, "search")))  # Wait for search box to be visible


# Function to search for products with a given query
def searchProducts(driver, searchQuery):
    login(driver, "nttn1234@gmail.com", "1234")  # Log in with the given credentials

    try:
        searchBox = searchBoxPresent(driver)  # Get the search box element
        searchBox.clear()  # Clear any pre-existing text in the search box
        searchBox.send_keys(searchQuery + Keys.RETURN)  # Input search query and press Enter
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "content")))  # Wait for the content to load
        driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='product-thumb']")  # Find all product elements
        time.sleep(2)  # Wait for results to load

        return getProductDetails(driver)  # Return the details of the products found
    except Exception as e:
        print(f"An error occurred: {e}")  # Print error if something goes wrong
        return []  # Return an empty list if an error occurs


# Function to extract details of the products found
def getProductDetails(driver):
    products = driver.find_elements(By.XPATH, "//div[@id='content']//div[@class='product-thumb']")  # Get all product elements
    productDetails = []  # Initialize an empty list to store product details

    if not products:
        print("No products found for the search query.")  # Print message if no products are found
        return productDetails  # Return empty list

    # Loop through each product and extract details
    for product in products:
        productName = product.find_element(By.XPATH, ".//h4/a").text  # Get the product name
        productPrice = product.find_element(By.XPATH, ".//span[@class='price-new']").text  # Get the product price
        productLink = product.find_element(By.XPATH, ".//h4/a").get_attribute('href')  # Get the product link

        # Append product details to the list
        productDetails.append({
            "name": productName,
            "price": productPrice,
            "link": productLink
        })

        # Print product details for debugging
        print(f"Product Name: {productName}")
        print(f"Price: {productPrice}")
        print(f"Link: {productLink}")
        print("=" * 40)

    return productDetails  # Return the list of product details


# Test case to verify correct search results for a product
def testCorrectSearchProducts(driver):
    existentKeyword = "Iphone"  # Search query for a valid product
    results = searchProducts(driver, existentKeyword)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) > 0, "No products found for 'Iphone'"  # Assert that products were found


# Test case to verify search with no results for a non-existent product
def testSearchWithNoExistProducts(driver):
    nonexistentKeyword = "KhongCoSanPham"  # Search query for a non-existent product
    results = searchProducts(driver, nonexistentKeyword)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) == 0, f"Expected no products for '{nonexistentKeyword}', but found some."  # Assert that no products were found


# Test case to verify search with uppercase letters
def testSearchWithUppercaseAllText(driver):
    uppercaseKeyword = "IPHONE"  # Search query with uppercase letters
    results = searchProducts(driver, uppercaseKeyword)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) > 0, f"Expected products for '{uppercaseKeyword}', but none were found."  # Assert that products were found
    print(f"Test for uppercase keyword '{uppercaseKeyword}' passed. Products found: {len(results)}.")  # Print success message


# Test case to verify search with lowercase letters
def testSearchWithLowercaseAllText(driver):
    lowercaseKeyword = "iphone"  # Search query with lowercase letters
    results = searchProducts(driver, lowercaseKeyword)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) > 0, f"Expected products for '{lowercaseKeyword}', but none were found."  # Assert that products were found
    print(f"Test for lowercase keyword '{lowercaseKeyword}' passed. Products found: {len(results)}.")  # Print success message


# Test case to verify search with special characters
def testSearchSpecialCharacters(driver):
    specialCharacterSearchQuery = "!@#$%^&*()_+"  # Search query with special characters
    results = searchProducts(driver, specialCharacterSearchQuery)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) == 0, f"Expected no products for the special character search, but found {len(results)} products."  # Assert no products were found
    print("Test for special character search passed. No products found.")  # Print success message


# Test case to verify search with leading and trailing whitespaces
def testSearchWithWhitespaceSurrounded(driver):
    keywordWithWhitespace = "  Iphone  "  # Search query with leading and trailing whitespaces
    results = searchProducts(driver, keywordWithWhitespace)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) > 0, f"Expected to find products for '{keywordWithWhitespace}', but found none."  # Assert that products were found
    print(f"Test for keyword surrounded by whitespace '{keywordWithWhitespace}' passed. Products found.")  # Print success message


# Test case to verify search with an empty query
def testSearchEmptyCharacters(driver):
    emptySearchQuery = ""  # Search query is empty
    results = searchProducts(driver, emptySearchQuery)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) == 0, f"Expected no products for an empty search, but found {len(results)} products."  # Assert no products were found
    print("Test for empty search characters passed. No products found.")  # Print success message


# Test case to verify search with special characters in the query
def testSearchWithSpecialCharacterInText(driver):
    specialCharactersKeyword = "!Iphone"  # Search query with special characters
    results = searchProducts(driver, specialCharactersKeyword)  # Perform the search
    time.sleep(2)  # Wait for results to load
    assert len(results) == 0, f"Expected no products for '{specialCharactersKeyword}', but found some."  # Assert no products were found
    print(f"Test for special characters keyword '{specialCharactersKeyword}' passed. No products found.")  # Print success message


# Test case to verify search with a long query
def testSearchWithLongCharacterInText(driver):
    specialCharactersKeyword = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"  # Long search query
    results = searchProducts(driver, specialCharactersKeyword)  # Perform the search

    assert len(results) == 0, f"Expected no products for '{specialCharactersKeyword}', but found some."  # Assert no products were found
    print(f"Test for special characters keyword '{specialCharactersKeyword}' passed. No products found.")  # Print success message

    pageWidth = driver.execute_script("return document.body.scrollWidth;")  # Get the page width
    viewportWidth = driver.execute_script("return window.innerWidth;")  # Get the viewport width
    
    assert pageWidth <= viewportWidth, "The page layout is broken and has horizontal scrolling."  # Assert that there is no horizontal scrolling

    print("Layout test passed. No horizontal scrolling is present.")  # Print success message
