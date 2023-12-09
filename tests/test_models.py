import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from app import app, db
from app.models import User, Recipe
from testing_config import TestingConfig


class RecipeModelTestCase(unittest.TestCase):
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

    def test_recipe_model(self):
        # Create a test user for the foreign key constraint in Recipe
        user = User(username='RecipeOwner')
        db.session.add(user)
        db.session.commit()

        # Test creating a Recipe with all fields
        recipe = Recipe(
            title='Test Recipe',
            description='Test Description',
            user_id=user.id,   # User-Recipe relationship
            ingredients='Test Ingredients',
            preparation_time=30,
            cooking_time=45,
            servings=4
        )
        db.session.add(recipe)
        db.session.commit()

        # Retrieve the recipe and verify all fields
        retrieved_recipe = Recipe.query.filter_by(title='Test Recipe').first()
        self.assertIsNotNone(retrieved_recipe)
        self.assertEqual(retrieved_recipe.description, 'Test Description')
        self.assertEqual(retrieved_recipe.user_id, user.id)
        self.assertEqual(retrieved_recipe.ingredients, 'Test Ingredients')
        self.assertEqual(retrieved_recipe.preparation_time, 30)
        self.assertEqual(retrieved_recipe.cooking_time, 45)
        self.assertEqual(retrieved_recipe.servings, 4)

    def test_user_model(self):
        user = User(username='TestUser')
        user.set_password('TestPassword')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password('TestPassword'))
        self.assertFalse(user.check_password('WrongPassword'))

if __name__ == '__main__':
    unittest.main()
