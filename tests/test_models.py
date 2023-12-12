import unittest
import mysql.connector
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import app, db, init_app
from app.models import User, Recipe
from testing_config import TestingConfig 

class RecipeModelTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        cls.create_test_db()

    @classmethod
    def tearDownClass(cls):
        cls.empty_test_tables()  # Empty the test tables 
        cls.app_context.pop()

    @classmethod
    def create_test_db(cls):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="efrei",
                password="mlinprod"
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS test_mycuisine_db")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_mycuisine_db.users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password_hash VARCHAR(512) NOT NULL,
                    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    profile_picture VARCHAR(256)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_mycuisine_db.recipe (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    user_id INT,
                    ingredients TEXT,
                    preparation_time INT,
                    cooking_time INT,
                    servings INT,
                    steps TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Failed to create test database: {}".format(err))
            exit(1)

    @classmethod
    def empty_test_tables(cls):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="efrei",
                password="mlinprod",
                database="test_mycuisine_db"  
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM recipe")  
            cursor.execute("DELETE FROM users")   
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Failed to empty test tables: {}".format(err))
            exit(1)

    def setUp(self):
        app.config.from_object(TestingConfig) 
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.create_test_db()  
    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_user_model(self):
        user = User(username='TestUser', email='testuser@example.com')
        user.set_password('TestPassword')
        db.session.add(user)
        db.session.commit()

        # verify user model functionality
        self.assertTrue(user.check_password('TestPassword'))
        self.assertFalse(user.check_password('WrongPassword'))
        self.assertEqual(user.email, 'testuser@example.com')

    def test_recipe_model(self):
        user = User(username='RecipeOwner', email='owner@example.com')
        user.set_password('OwnerPassword')
        db.session.add(user)
        db.session.commit()

        # Create a test recipe
        recipe = Recipe(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredients',
            preparation_time=30,
            cooking_time=45,
            servings=4,
            user_id=user.id,
            steps='Test Steps'
        )
        db.session.add(recipe)
        db.session.commit()

        # Retrieve the recipe and verify its properties
        retrieved_recipe = Recipe.query.filter_by(title='Test Recipe').first()
        self.assertIsNotNone(retrieved_recipe)
        self.assertEqual(retrieved_recipe.description, 'Test Description')
        self.assertEqual(retrieved_recipe.user_id, user.id)
        self.assertEqual(retrieved_recipe.ingredients, 'Test Ingredients')
        self.assertEqual(retrieved_recipe.preparation_time, 30)
        self.assertEqual(retrieved_recipe.cooking_time, 45)
        self.assertEqual(retrieved_recipe.servings, 4)
        self.assertEqual(retrieved_recipe.steps, 'Test Steps')

if __name__ == '__main__':
    unittest.main()
