import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import app, db
from app.models import User, Recipe
from app.forms import RegistrationForm, LoginForm, RecipeForm
from testing_config import TestingConfig
from flask_testing import TestCase  

class RecipeIntegrationTestCase(TestCase):
    def create_app(self):
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()  

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)  

    def test_view_recipe(self):
        user = User(username='RecipeOwner', email='owner@example.com')
        user.set_password('password')  
        db.session.add(user)
        db.session.commit()

        # Create a test recipe
        recipe = Recipe(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredient 1\nTest Ingredient 2',
            preparation_time=30,
            cooking_time=45,
            servings=4,
            user_id=user.id,
            steps='Step 1: Do this\nStep 2: Do that',
        )

        db.session.add(recipe)
        db.session.commit()

        response = self.client.get(f'/recipe/{recipe.id}')
        self.assert200(response)  

    def test_user_registration(self):
        data = {'username': 'testuser', 'password': 'password', 'email': 'testuser@example.com'}
        response = self.client.post('/register', data=data, follow_redirects=True)
        self.assert200(response)  

    def test_user_login(self):
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('password')  
        db.session.add(user)
        db.session.commit()

        data = {'username': 'testuser', 'password': 'password'}
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assert200(response)  

    def test_user_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assert200(response)  

    def test_add_recipe(self):
        user = User(username='RecipeOwner', email='owner@example.com')
        user.set_password('password')  
        db.session.add(user)
        db.session.commit()

        data = {
            'title': 'Test Recipe',
            'description': 'Test Description',
            'ingredients': 'Test Ingredient 1\nTest Ingredient 2',
            'preparation_time': 30,
            'cooking_time': 45,
            'servings': 4,
            'steps': 'Step 1: Do this\nStep 2: Do that',
        }
        with self.client:
            self.client.post('/login', data={'username': 'RecipeOwner', 'password': 'password'})
            response = self.client.post('/recipe/add', data=data, follow_redirects=True)
            self.assert200(response)  

    def test_edit_recipe(self):
        user = User(username='RecipeOwner', email='owner@example.com')
        user.set_password('password')  
        db.session.add(user)
        db.session.commit()

        # Create a test recipe
        recipe = Recipe(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredient 1\nTest Ingredient 2',
            preparation_time=30,
            cooking_time=45,
            servings=4,
            user_id=user.id,
            steps='Step 1: Do this\nStep 2: Do that',
        )

        db.session.add(recipe)
        db.session.commit()

        data = {
            'title': 'Updated Recipe',
            'description': 'Updated Description',
            'ingredients': 'Updated Ingredient 1\nUpdated Ingredient 2',
            'preparation_time': 60,
            'cooking_time': 30,
            'servings': 6,
            'steps': 'Updated Step 1: Do this\nUpdated Step 2: Do that',
        }
        with self.client:
            self.client.post('/login', data={'username': 'RecipeOwner', 'password': 'password'})
            response = self.client.post(f'/recipe/edit/{recipe.id}', data=data, follow_redirects=True)
            self.assert200(response)  

    def test_delete_recipe(self):
        user = User(username='RecipeOwner', email='owner@example.com')
        user.set_password('password')  
        db.session.add(user)
        db.session.commit()

        # Create a test recipe
        recipe = Recipe(
            title='Test Recipe',
            description='Test Description',
            ingredients='Test Ingredient 1\nTest Ingredient 2',
            preparation_time=30,
            cooking_time=45,
            servings=4,
            user_id=user.id,
            steps='Step 1: Do this\nStep 2: Do that',
        )

        db.session.add(recipe)
        db.session.commit()

        with self.client:
            self.client.post('/login', data={'username': 'RecipeOwner', 'password': 'password'})
            response = self.client.post(f'/recipe/delete/{recipe.id}', follow_redirects=True)
            self.assert200(response)  

if __name__ == '__main__':
    unittest.main()
