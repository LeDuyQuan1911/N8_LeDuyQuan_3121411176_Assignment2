import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging

logging.basicConfig(level=logging.ERROR)

# Thiết lập fixture để khởi tạo và đóng trình duyệt
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  
    yield driver
    driver.quit()

# Function to login to the page
def login(driver, email, password):
    driver.get("http://localhost/webopencart/index.php?route=account/login&language=en-gb")
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "input-email"))).send_keys(email)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()

# Function to check login success
def check_login_success(driver):
    WebDriverWait(driver, 3).until(EC.url_contains("account/account"))
    assert "account/account" in driver.current_url, "Login failed or user not redirected to account page."

# Function to log out from the account
def logout(driver):
    account_dropdown = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='dropdown-toggle' and @data-bs-toggle='dropdown']")))
    driver.execute_script("arguments[0].click();", account_dropdown)
    
    logout_link = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    driver.execute_script("arguments[0].click();", logout_link)
    
    notification = driver.find_element(By.CSS_SELECTOR, "#content > h1")  # Locate the order confirmation notification
    notificationActual = notification.text  # Get the actual notification text
    notificationExpected = "Account Logout"  # Expected notification text
    assert notificationExpected == notificationActual, "Order was not placed successfully"  # Assert that the order was placed successfully

# Function to check for error message
def check_error_message(driver, expected_message):
    error_message = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
    assert error_message.is_displayed(), "Error message is not displayed."
    assert expected_message in error_message.text.strip(), "Unexpected error message content."

# Test login and logout process
def testLoginAndCheckOut(driver):
    login(driver, "leduyquan2574@gmail.com", "Quan19112003")
    time.sleep(5)
    check_login_success(driver)
    logout(driver)

# Test login with wrong email format
def testWrongEmailLogin(driver):
    login(driver, "wrongemail.com", "wrongpassword")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test login with incorrect password
def testInvalidWrongLogin(driver):
    login(driver, "leduyquan2574@gmail.com", "wrongpassword")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test login with empty password field
def testEmptyPasswordLogin(driver):
    login(driver, "nttn1234@gmail.com", "")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test login with empty email field
def testEmptyEmailLogin(driver):
    login(driver, "", "wrongpassword")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test login with special characters in email
def testSpecialCharacterEmailLogin(driver):
    login(driver, "!@#$%^&*()", "password")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test login with special characters in password
def testSpecialCharacterPasswordLogin(driver):
    login(driver, "leduyquan2574@gmail.com", "!@#$%^&*()")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test login with both email and password containing special characters
def testSpecialCharacterPasswordAndEmailLogin(driver):
    login(driver, "!@#$%^&*()", "!@#$%^&*()")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")

# Test SQL injection attempt in login
def testSqlInvalidToLogin(driver):
    login(driver, "' UNION SELECT NULL, username, password FROM users -- ", "' UNION SELECT NULL, username, password FROM users -- ")
    check_error_message(driver, "Warning: No match for E-Mail Address and/or Password.")
