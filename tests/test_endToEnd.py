import mysql.connector
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

        # Create the 'test_mycuisine_db' database for testing
        cls.create_test_database()

    @classmethod
    def tearDownClass(cls):
        """
        Terminate the application server and delete the test database after tests complete.
        """
        cls.server.terminate()
        cls.server.wait()

        # Delete the 'test_mycuisine_db' database
        cls.delete_test_database()

    @classmethod
    def setUp(cls):
        """
        Set up the test environment by initializing the Chrome WebDriver and opening the base URL.
        """
        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.driver.get(BASE_URL)

    @classmethod
    def tearDown(cls):
        """
        Clean up the test environment by quitting the WebDriver.
        """
        cls.driver.quit()

    @classmethod
    def create_test_database(cls):
        """
        Create the 'test_mycuisine_db' database for testing.
        """
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Replace with your MySQL host
                user='efrei',      # Replace with your MySQL user
                password='mlinprod'  # Replace with your MySQL password
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS test_mycuisine_db")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete_test_database(cls):
        """
        Delete the 'test_mycuisine_db' database after testing.
        """
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Replace with your MySQL host
                user='efrei',      # Replace with your MySQL user
                password='mlinprod'  # Replace with your MySQL password
            )
            cursor = connection.cursor()
            cursor.execute("DROP DATABASE IF EXISTS test_mycuisine_db")
        finally:
            cursor.close()
            connection.close()

    def test_register_and_login(self):
        """
        Test the registration and login functionality.
        """
        # Check if the user already exists and delete them if necessary
        if self.user_exists('test_user'):
            self.delete_user('test_user')

        # Navigate to the registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Fill out the registration form
        self.register_user()

        # Check if registration was successful
        success_message = 'Congratulations, you are now a registered user!'
        self.assertTrue(self.is_element_present(By.CLASS_NAME, 'success-message-class'))
        self.assertEqual(success_message, self.get_page_content())

        # Navigate to the login page
        self.driver.find_element(By.LINK_TEXT, 'Sign In').click()

        # Fill out the login form
        self.login_user()

        # Check if login was successful
        welcome_message = 'Welcome'
        self.assertTrue(self.is_element_present(By.PARTIAL_LINK_TEXT, welcome_message))
        self.assertEqual(welcome_message, self.get_page_content())

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

    def user_exists(self, username):
        """
        Check if a user with the given username already exists in the MySQL database.
        """
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Replace with your MySQL host
                user='efrei',  # Replace with your MySQL user
                password='mlinprod',  # Replace with your MySQL password
                database='test_mycuisine_db'  # Replace with your MySQL database name
            )

            cursor = connection.cursor()
            query = "SELECT username FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result is not None
        finally:
            cursor.close()
            connection.close()

    def delete_user(self, username):
        """
        Delete a user with the given username from the MySQL database.
        """
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Replace with your MySQL host
                user='efrei',  # Replace with your MySQL user
                password='mlinprod',  # Replace with your MySQL password
                database='test_mycuisine_db'  # Replace with your MySQL database name
            )

            cursor = connection.cursor()
            query = "DELETE FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    unittest.main()
