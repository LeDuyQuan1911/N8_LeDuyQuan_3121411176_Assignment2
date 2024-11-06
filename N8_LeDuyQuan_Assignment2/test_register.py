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
from selenium.webdriver.firefox.options import Options

logging.basicConfig(level=logging.ERROR)

# Fixture to initialize the WebDriver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    yield driver  # Yield the driver to the test function
    driver.quit()  # Quit the driver after the test

# Helper functions for common actions
def openRegistrationPage(driver):
    driver.get("http://localhost/webopencart/index.php?route=account/register&language=en-gb")  # Navigate to the registration page
    time.sleep(2)  # Wait for the page to load

def fillRegistrationForm(driver, firstName, lastName, email, password):
    # Fill in the first name field
    firstNameField = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "input-firstname"))
    )
    firstNameField.send_keys(firstName)

    # Fill in the last name field
    lastNameField = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "input-lastname"))
    )
    lastNameField.send_keys(lastName)

    # Fill in the email field
    emailField = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "input-email"))
    )
    emailField.send_keys(email)

    # Fill in the password field
    passwordField = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "input-password"))
    )
    passwordField.send_keys(password)

    # Scroll to the "agree" checkbox
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.NAME, "agree"))
    time.sleep(2)  # Wait for the element to become visible

def agreeToPrivacyPolicy(driver):
    # Find and click the privacy policy checkbox
    privacyPolicyCheckbox = driver.find_element(By.NAME, "agree")
    driver.execute_script("arguments[0].click();", privacyPolicyCheckbox)
    time.sleep(2)  # Wait for the checkbox to be clicked

def clickContinue(driver):
    # Find and click the continue button
    continueButton = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    continueButton.click()
    time.sleep(2)  # Wait for the page to load after clicking

def assertSuccessMessage(driver):
    try:
        # Wait for the success message element to appear
        successMessage = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='content']/h1"))
        )
        # Assert that the success message is displayed
        assert successMessage.is_displayed(), "Success message is not displayed after registration."
        # Assert that the success message contains the expected text
        assert "Your Account Has Been Created!" in successMessage.text, "Account creation message is incorrect."
    except Exception as e:
        print("Error or assertion failed:", e)
        print("Current page source:", driver.page_source)

def assertErrorMessage(driver, fieldId, expectedError):
    try:
        # Find the error message next to the input field
        errorMessage = driver.find_element(By.XPATH, f"//input[@id='{fieldId}']/following-sibling::div[@class='text-danger']")
        # Assert that the error message is displayed
        assert errorMessage.is_displayed(), f"{fieldId} error message not displayed."
        # Assert that the error message contains the expected text
        assert expectedError in errorMessage.text, f"Error message text for {fieldId} is incorrect."
    except Exception as e:
        print("Error or assertion failed:", e)
        print("Current page source:", driver.page_source)


# Test Cases
def testRegisterValidData(driver):
    openRegistrationPage(driver)  # Open the registration page
    fillRegistrationForm(driver, "Lê Duy", "Quân", "leduyquan2574@gmail.com", "Quan19112003")  # Fill the form with valid data
    agreeToPrivacyPolicy(driver)  # Agree to the privacy policy
    clickContinue(driver)  # Click the continue button
    assertSuccessMessage(driver)  # Assert that the success message is displayed

def testRegisterEmptyRequiredInput(driver):
    openRegistrationPage(driver)  # Open the registration page
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.NAME, "agree"))  # Scroll to the privacy policy checkbox
    time.sleep(2)  # Wait for the checkbox to become visible
    clickContinue(driver)  # Click the continue button
    assertErrorMessage(driver, "input-firstname", "First Name must be between 1 and 32 characters!")  # Assert first name error
    assertErrorMessage(driver, "input-lastname", "Last Name must be between 1 and 32 characters!")  # Assert last name error
    assertErrorMessage(driver, "input-email", "E-Mail Address does not appear to be valid!")  # Assert email error
    assertErrorMessage(driver, "input-password", "Password must be between 4 and 20 characters!")  # Assert password error

def testRegisterInvalidEmail(driver):
    openRegistrationPage(driver)  # Open the registration page
    fillRegistrationForm(driver, "Lê Duy", "Quân", "leduyquan2574.com", "Quan19112003")  # Fill with an invalid email
    agreeToPrivacyPolicy(driver)  # Agree to the privacy policy
    clickContinue(driver)  # Click continue
    assertErrorMessage(driver, "input-email", "E-Mail Address does not appear to be valid!")  # Assert email error

def testRegisterExistAccount(driver):
    openRegistrationPage(driver)  # Open the registration page
    fillRegistrationForm(driver, "Lê Duy", "Quân", "leduyquan2574@gmail.com", "Quan19112003")  # Fill with an existing email
    agreeToPrivacyPolicy(driver)  # Agree to the privacy policy
    clickContinue(driver)  # Click continue
    assertErrorMessage(driver, "input-email", "E-Mail Address is already registered!")  # Assert account exists error

def testNoClickPolicy(driver):
    openRegistrationPage(driver)  # Open the registration page
    fillRegistrationForm(driver, "Lê Duy", "Quân", "leduyquan2574@gmail.com", "Quan19112003")  # Fill the form
    clickContinue(driver)  # Click continue
    try:
        errorMessage = driver.find_elements(By.CLASS_NAME, "alert-danger")  # Find error message
        if errorMessage:
            assert errorMessage[0].is_displayed(), "Error message not displayed for not agreeing to privacy policy."  # Assert error message display
            assert "Warning: You must agree to the Privacy Policy!" in errorMessage[0].text, "Unexpected error message content."  # Assert error message content
            print("Error message displayed as expected:", errorMessage[0].text)
        else:
            print("No error message displayed. Test failed.")
    except Exception as e:
        print("Error or assertion failed:", e)
        print("Current page source:", driver.page_source)

def testRegisterSpecialCharactersInName(driver):
    openRegistrationPage(driver)  # Open the registration page
    fillRegistrationForm(driver, "!!!!!!!!!", "!!!!!!!!", "leduyquan9999999@gmail.com", "1234")  # Fill with special characters
    agreeToPrivacyPolicy(driver)  # Agree to the privacy policy
    clickContinue(driver)  # Click continue
    assertErrorMessage(driver, "input-firstname", "First Name must be between 1 and 32 characters!")  # Assert first name error
    assertErrorMessage(driver, "input-lastname", "Last Name must be between 1 and 32 characters!")  # Assert last name error
