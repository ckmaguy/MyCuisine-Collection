from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Recipe
from app.forms import LoginForm, RegistrationForm, RecipeForm

@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', title='Home', recipes=recipes)

@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', title=recipe.title, recipe=recipe)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.')
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!','success-message-class')
                return redirect(url_for('login'))
            except Exception as e:
                # Print any exception for debugging 
                print(f"Error during registration: {str(e)}")
                flash('An error occurred during registration. Please try again later.')

    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password','error-message-class')
            return redirect(url_for('login'))
        login_user(user)
        flash('You have successfully logged in.', 'success-message-class')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/recipe/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data, 
            description=form.description.data,
            ingredients=form.ingredients.data,
            preparation_time=form.preparation_time.data,
            cooking_time=form.cooking_time.data,
            servings=form.servings.data,
            steps=form.steps.data,
            user_id=current_user.id
            
        )  
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been added!')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', title='New Recipe', form=form)

@app.route('/recipe/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if current_user != recipe.user:
        flash('You are not authorized to edit this recipe.')
        return redirect(url_for('index'))

    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.preparation_time = form.preparation_time.data
        recipe.cooking_time = form.cooking_time.data
        recipe.servings = form.servings.data
        recipe.steps = form.steps.data
        
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))

    return render_template('edit_recipe.html', title='Edit Recipe', form=form)

@app.route('/recipe/delete/<int:id>', methods=['POST'])
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if current_user != recipe.user:
        flash('You are not authorized to delete this recipe.')
        return redirect(url_for('index'))
    
    db.session.delete(recipe)
    db.session.commit()
    flash('The recipe has been deleted.')
    return redirect(url_for('index'))
