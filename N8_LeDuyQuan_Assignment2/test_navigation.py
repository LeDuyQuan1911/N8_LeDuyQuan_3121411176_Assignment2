import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# Define a fixture to initialize the driver and quit it after tests
@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()  # Initialize the webdriver instance
    yield driver  # Yield the driver to the test
    driver.quit()  # Quit the driver after the test

class TestNavigation:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver  # Assign the driver to the instance variable
        self.wait = WebDriverWait(driver, 10)  # Wait for elements with a timeout of 10 seconds
        self.driver.get('http://localhost/webopencart/index.php?route=common/home&language=en-gb')  # Navigate to the home page

    def testClickDesktopsAndMac(self):
        # Click on "Desktops" in the navbar
        desktopsMenu = self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle[href*="category"]')
        desktopsMenu.click()

        # Click on "Mac" in the dropdown of "Desktops"
        # Locate and click the link using CSS selector matching href and class attributes
        macSubcategory = self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href*="category&language=en-gb&path=20_27"]')
        macSubcategory.click()

        # Verify that the page title contains "Mac"
        assert 'Mac' in self.driver.title

    def testShowAllDesktops(self):
        # Click on "Desktops" and then "Show All Desktops"
        self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle[href*="category"]').click()
        showAllLink = self.driver.find_element(By.CSS_SELECTOR, 'a.see-all[href*="category"]')
        showAllLink.click()

        # Verify that the page title contains "Desktops"
        assert 'Desktops' in self.driver.title

    def testMenuNavigation(self):
        # Click on the "Desktops" menu item
        desktopsMenu = self.driver.find_element(By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle[href*="category"]')
        desktopsMenu.click()

        # Define menu items and their sub-items to iterate through
        menuItems = [
            {"name": "Desktops", "subItems": ["PC (0)", "Mac (1)"]},
            {"name": "Laptops & Notebooks", "subItems": ["Macs (0)", "Windows (0)"]},
            {"name": "Components", "subItems": ["Mice and Trackballs (0)", "Monitors (2)", "Printers (0)", "Scanners (0)", "Web Cameras (0)"]},
            {"name": "MP3 Players", "subItems": ["test 11 (0)", "test 12 (0)", "test 15 (0)"]}
        ]

        # Loop through the main menu items
        for item in menuItems:
            # Hover over the main menu item
            menu = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, item["name"])))
            ActionChains(self.driver).move_to_element(menu).perform()  # Hover over the menu item
            self.wait.until(EC.visibility_of(menu))  # Wait until the menu is visible

            # Loop through each sub-item and click it
            for subItem in item["subItems"]:
                subMenu = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, subItem)))  # Wait for sub-item to be clickable
                subMenu.click()  # Click on the sub-item

                # Verify navigation by checking the page title
                expectedTitle = subItem.split(" ")[0]  # Extract the expected title from the sub-item text
                assert expectedTitle in self.driver.title, f"Expected title to include {expectedTitle}"  # Assert that the title matches

                # Navigate back to the previous page
                self.driver.back()

                # Re-hover over the main menu item to reopen it after navigating back
                menu = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, item["name"])))
                ActionChains(self.driver).move_to_element(menu).perform()
