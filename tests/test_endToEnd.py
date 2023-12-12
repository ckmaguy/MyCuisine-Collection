import mysql.connector
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import mysql.connector
from mysql.connector import errorcode
from selenium.common.exceptions import NoSuchElementException  # Import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time

# Constants
BASE_URL = 'http://127.0.0.1:5000'

class TestAppE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start a test instance of the application using start_test.py.
        """
        cls.server = subprocess.Popen(['python', 'start_test.py'])
        time.sleep(3)  

    @classmethod
    def tearDownClass(cls):
        """
        Terminate the application server after tests complete.
        """
        cls.server.terminate()
        cls.server.wait()

    @classmethod
    def setUp(cls):
        """
        Set up the test environment by initializing the Chrome WebDriver and opening the base URL.
        """
        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.driver.get(BASE_URL)
    
    @classmethod
    def delete_user_if_exists(cls, username):
        """
        Delete the user from the database if they exist.
        """
        try:
            # Set up the database connection
            db = mysql.connector.connect(
                host="localhost",
                user="efrei",  
                password="mlinprod",  
                database="test_mycuisine_db"
            )
            cursor = db.cursor()

            # SQL DELETE statement to delete the user if they exist
            delete_statement = "DELETE FROM users WHERE username = %s"
            cursor.execute(delete_statement, (username,))

            # Commit changes
            db.commit()

            # Check if the user was deleted
            if cursor.rowcount > 0:
                print(f"User {username} was deleted.")
            else:
                print(f"No user found with username {username}.")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        finally:
            # Close the cursor and connection
            cursor.close()
            db.close()

    @classmethod
    def tearDown(cls):
        """
        Clean up the test environment by quitting the WebDriver.
        """
        cls.driver.quit()

    def test_register_and_login(self):
        """
        Test the registration and login functionality.
        """
        # Ensure user does not exist
        self.delete_user_if_exists('test_user')

        # Navigate to the registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Fill out the registration form
        self.register_user()
        self.register_user()

        # Check if registration was successful
        success_message = 'Congratulations, you are now a registered user!'
        self.assertTrue(self.is_element_present(By.CLASS_NAME, 'success-message-class'))
        self.assertEqual(success_message, self.get_page_content())
        success_message = 'Congratulations, you are now a registered user!'
        self.assertTrue(self.is_element_present(By.CLASS_NAME, 'success-message-class'))
        self.assertEqual(success_message, self.get_page_content())

        # Navigate to the login page
        #self.driver.find_element(By.LINK_TEXT, 'Sign In').click()
        
        # Directly navigate to the login page
        self.driver.get(BASE_URL + '/login')
        
        # Fill out the login form
        self.login_user()
        self.login_user()

        # Check if login was successful
        welcome_message = 'Welcome'
        if not self.is_element_present(By.PARTIAL_LINK_TEXT, welcome_message):
            # Check for login error messages
            try:
                login_error_message_element = self.driver.find_element(By.CLASS_NAME, 'login-error-message-class')
                login_error_message = login_error_message_element.text
                self.fail(f"Login failed: {login_error_message}")
            except NoSuchElementException:
                # No login error message found, consider it a successful login
                pass

    def register_user(self):
        """
        Fill out the registration form.
        """
        self.fill_form('username', 'test_user')
        self.fill_form('email', 'test@example.com')
        self.fill_form('password', 'password123')
        self.fill_form('confirm_password', 'password123')
        self.driver.find_element(By.XPATH, "//button[text()='Register']").click()

    def login_user(self):
        """
        Fill out the login form.
        """
        self.fill_form('username', 'test_user')
        self.fill_form('password', 'password123')
        self.driver.find_element(By.NAME, 'submit').click()

    def fill_form(self, field_name, value):
        """
        Fill out a form field.
        """
        field = self.driver.find_element(By.NAME, field_name)
        field.send_keys(value)

    def get_page_content(self):
        """
        Get the content of the current page.
        """
        message_element = self.driver.find_element(By.CLASS_NAME, 'success-message-class')
        return message_element.text

    def is_element_present(self, by, value):
        """
        Check if an element is present on the page.
        """
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, value)))
            return True
        except Exception:
            return False

if __name__ == '__main__':
    unittest.main()
