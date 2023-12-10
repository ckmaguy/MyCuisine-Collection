import unittest
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import app, db  
from app.models import User, Recipe  
from testing_config import TestingConfig  

class RecipeModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestingConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model(self):
        user = User(username='TestUser', email='testuser@example.com')
        user.set_password('TestPassword')
        db.session.add(user)
        db.session.commit()

        # Assertions to verify user model functionality
        self.assertTrue(user.check_password('TestPassword'))
        self.assertFalse(user.check_password('WrongPassword'))
        self.assertEqual(user.email, 'testuser@example.com')

    def test_recipe_model(self):
        user = User(username='RecipeOwner', email='owner@example.com')
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
            steps='Test Steps'  # Adding the steps field
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
