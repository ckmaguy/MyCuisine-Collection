import unittest
from msedge.selenium_tools import Edge, EdgeOptions

# Constants
EDGEDRIVER_PATH = r'C:\Users\EFREI\Desktop\M2\S9\ML in Production\Project\MyCuisine-Collection\msedgedriver.exe'
BASE_URL = 'http://127.0.0.1:5000'
USERNAME = 'test_user'
EMAIL = 'test@example.com'
PASSWORD = 'password123'

class TestAppE2E(unittest.TestCase):
    def setUp(self):
        # Create EdgeOptions
        edge_options = EdgeOptions()
        edge_options.use_chromium = True  # Use Chromium-based Edge
        edge_options.binary_location = EDGEDRIVER_PATH

        # Initialize the Edge WebDriver
        self.driver = Edge(executable_path=EDGEDRIVER_PATH, options=edge_options)
        self.driver.get(BASE_URL)

    def test_register_and_login(self):
        # Navigate to the registration page
        self.driver.find_element_by_link_text('Register').click()

        # Fill out the registration form
        username_field = self.driver.find_element_by_name('username')
        email_field = self.driver.find_element_by_name('email')
        password_field = self.driver.find_element_by_name('password')
        confirm_password_field = self.driver.find_element_by_name('confirm_password')

        username_field.send_keys(USERNAME)
        email_field.send_keys(EMAIL)
        password_field.send_keys(PASSWORD)
        confirm_password_field.send_keys(PASSWORD)

        self.driver.find_element_by_name('submit').click()

        # Check if registration was successful
        self.assertIn('Congratulations, you are now a registered user!', self.driver.page_source)

        # Navigate to the login page
        self.driver.find_element_by_link_text('Sign In').click()

        # Fill out the login form
        username_field = self.driver.find_element_by_name('username')
        password_field = self.driver.find_element_by_name('password')

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)

        self.driver.find_element_by_name('submit').click()

        # Check if login was successful
        self.assertIn('Welcome', self.driver.page_source)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
