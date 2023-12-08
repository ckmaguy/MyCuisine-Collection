import unittest
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

    def test_recipe_model(self):
        recipe = Recipe(title='Test Recipe', description='Test Description')
        db.session.add(recipe)
        db.session.commit()
        self.assertEqual(recipe.title, 'Test Recipe')

    def test_user_model(self):
        user = User(username='TestUser')
        user.set_password('TestPassword')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password('TestPassword'))
        self.assertFalse(user.check_password('WrongPassword'))
