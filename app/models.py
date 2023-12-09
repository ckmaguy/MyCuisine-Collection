from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)  
    password_hash = db.Column(db.String(128))
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())  
    profile_picture = db.Column(db.String(256))  

    # Relationship to link user with their recipes
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text)  
    preparation_time = db.Column(db.Integer)  
    cooking_time = db.Column(db.Integer)  
    servings = db.Column(db.Integer) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  

    def __repr__(self):
        return f'<Recipe {self.title}>'
