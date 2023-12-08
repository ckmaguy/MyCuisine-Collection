import unittest
from app import app, db  
from app.models import User, Recipe
from testing_config import TestingConfig
from flask import url_for

class RecipeIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestingConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_recipe(self):
        recipe = Recipe(title='Test Recipe', description='Test Description')
        db.session.add(recipe)
        db.session.commit()
        response = self.client.get(url_for('view_recipe', id=recipe.id))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post(url_for('register'), data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
