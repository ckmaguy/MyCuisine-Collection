import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import app, db  
from app.models import User, Recipe
from testing_config import TestingConfig

class E2ETestCase(unittest.TestCase):
    def setUp(self):
        
        app.config.from_object(TestingConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_and_add_recipe(self):
        # Create a test user
        user = User(username='testuser')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        # Log in
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('password')
        self.driver.find_element(By.NAME, 'submit').click()

        # Add a recipe
        self.driver.get('http://localhost:5000/add_recipe')
        self.driver.find_element(By.NAME, 'title').send_keys('Test Recipe')
        self.driver.find_element(By.NAME, 'description').send_keys('Test description')
        self.driver.find_element(By.NAME, 'submit').click()

        # Check if the recipe is in the database
        retrieved_recipe = Recipe.query.first()
        self.assertEqual(retrieved_recipe.title, 'Test Recipe')
