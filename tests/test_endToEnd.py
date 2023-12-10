import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Constants
BASE_URL = 'http://127.0.0.1:5000'
USERNAME = 'test_user'
EMAIL = 'test@example.com'
PASSWORD = 'password123'

class TestAppE2E(unittest.TestCase):
    def setUp(self):
        # Initialize the Chrome WebDriver using WebDriverManager
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(BASE_URL)

    def wait_for_element(self, by, value, timeout=30):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value)))

    def test_register_and_login(self):
        # Wait for the registration link to be clickable
        registration_link = self.wait_for_element(By.LINK_TEXT, 'Register')
        registration_link.click()

        # Fill out the registration form
        username_field = self.wait_for_element(By.NAME, 'username')
        email_field = self.driver.find_element(By.NAME, 'email')
        password_field = self.driver.find_element(By.NAME, 'password')
        confirm_password_field = self.driver.find_element(By.NAME, 'confirm_password')

        username_field.send_keys(USERNAME)
        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)
        confirm_password_field.send_keys(PASSWORD)

        # Wait for the submit button to be clickable
        submit_button = self.wait_for_element(By.NAME, 'submit')
        submit_button.click()

        # Check if registration was successful
        self.assertIn('Congratulations, you are now a registered user!', self.driver.page_source)

        # Navigate to the login page
        login_link = self.wait_for_element(By.LINK_TEXT, 'Sign In')
        login_link.click()

        # Fill out the login form
        username_field = self.wait_for_element(By.NAME, 'username')
        password_field = self.driver.find_element(By.NAME, 'password')

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)

        # Wait for the submit button to be clickable
        submit_button = self.wait_for_element(By.NAME, 'submit')
        submit_button.click()

        # Check if login was successful
        self.assertIn('Welcome', self.driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
