from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from datetime import datetime 
import secrets
import os

# clone github directory with "git clone https://github.com/KolozsiZsombor/SzoftverModszerMiniProject"
# cmd : "pip install flask"
# go into directory with cd /SzoftverModszerMiniProject
# run python script with python app.py
# visit http://127.0.0.1:5000
# stop server with ctrl + c


##SETUPS AND INITIALIZATIONS
app = Flask(__name__)

db = SQLAlchemy()

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

users_db = {} #simulate database

bcrypt = Bcrypt(app)  # Initialize Bcrypt

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Set up SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Initialize SQLAlchemy

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login if not authenticated

# Database Models

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='normal', nullable=False)  # Role can be 'admin' or 'normal'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Record creation date
    jokes = db.relationship('Joke', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Category of the joke
    content = db.Column(db.Text, nullable=False)  # Content of the joke
    rating = db.Column(db.Float, default=0)  # Overall rating for the joke
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Joke creation date
    approved = db.Column(db.Boolean, default=False)  # Approval status of the joke
    comments = db.relationship('Comment', backref='joke', lazy=True)
    ratings = db.relationship('Rating', backref='joke', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joke_id = db.Column(db.Integer, db.ForeignKey('joke.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)  # Text of the comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Comment creation date

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joke_id = db.Column(db.Integer, db.ForeignKey('joke.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Rating (1 character int, typically 1-5)

with app.app_context():
    db.create_all()

# Implementing required methods from UserMixin
    @property
    def is_active(self):
        return True  # Implement your logic if users can be inactive

    @property
    def is_authenticated(self):
        return True  # Users are authenticated once logged in

    @property
    def is_anonymous(self):
        return False  # Users cannot be anonymous once logged in

# Define forms
class JokeSubmissionForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(max=50)])
    content = TextAreaField('Joke Content', validators=[DataRequired()])
    submit = SubmitField('Submit Joke')

class CommentForm(FlaskForm):
    comment_text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')

class RatingForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
               
@app.route('/')
def home():
    if current_user.is_authenticated and current_user.role == 'admin':
        jokes = Joke.query.all()  # Admins see all jokes
    else:
        jokes = Joke.query.filter_by(approved=True).all()  # Non-admins see only approved jokes

    return render_template('index.html', jokes=jokes)





login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
### Registration 
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name',validators=[DataRequired(), Length(min=6, max=32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    role = SelectField('Role', choices=[('normal', 'Normal User'), ('admin', 'Admin User')], default='normal')
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        role = form.role.data
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create a new user and add to the database
        new_user = User(email=email, name=name, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', form=form)
### end of registration

### Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])  # Only DataRequired
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect if already logged in

    form = LoginForm()
    if form.validate_on_submit():  # Check if form is submitted and valid
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()  # Get the user by email
        
        # Check if the user exists and the password matches
        if user and bcrypt.check_password_hash(user.password_hash, password):  # Ensure you have a method to check password
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to index or home
        else:
            flash('Login failed. Check your email and password.', 'danger')

    return render_template('login.html', form=form)

### end of Login
@app.route('/logout')
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))  # Redirect to home after logging out

@app.route('/submit_joke', methods=['GET', 'POST'])
@login_required
def submit_joke():
    if request.method == 'POST':
        category = request.form.get('category')
        content = request.form.get('content')  # Get the content from the form
        
        if content:  # Ensure content is provided
            new_joke = Joke(
                user_id=current_user.id,
                category=category,
                content=content,  # Assign the content to the new joke
                rating=0.0,  # Set default rating or modify as necessary
                approved=True  # Automatically approve the joke upon creation
            )
            db.session.add(new_joke)
            db.session.commit()

            flash('Joke submitted successfully and is approved.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Content cannot be empty!', 'danger')

    return render_template('submit_joke.html')



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')





@app.route('/joke/<int:joke_id>', methods=['GET', 'POST'])
def joke_detail(joke_id):
    joke = Joke.query.get_or_404(joke_id)
    form_comment = CommentForm()
    form_rating = RatingForm()
    
    if form_comment.validate_on_submit():
        comment_text = form_comment.comment_text.data
        new_comment = Comment(user_id=1, joke_id=joke.id, comment_text=comment_text)  # Replace '1' with current user ID
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('joke_detail', joke_id=joke.id))
    
    if form_rating.validate_on_submit():
        rating_value = form_rating.rating.data
        new_rating = Rating(user_id=1, joke_id=joke.id, rating=rating_value)  # Replace '1' with current user ID
        db.session.add(new_rating)
        db.session.commit()
        flash('Rating submitted!', 'success')
        return redirect(url_for('joke_detail', joke_id=joke.id))

    comments = Comment.query.filter_by(joke_id=joke.id).all()
    return render_template('joke_detail.html', joke=joke, form_comment=form_comment, form_rating=form_rating, comments=comments)

### Admin stuff begins here
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    jokes = Joke.query.all()  # Fetch all jokes from the database
    users = User.query.all()  # Fetch all users from the database
    return render_template('admin.html', jokes=jokes, users=users)

@app.route('/admin/delete/<int:joke_id>', methods=['POST'])
@login_required
def delete_joke(joke_id):
    if current_user.role != 'admin':  # Check if the user is an admin
        flash('You do not have permission to delete this joke.', 'danger')
        return redirect(url_for('home'))

    joke = Joke.query.get(joke_id)  # Fetch the joke by ID
    if joke:
        db.session.delete(joke)  # Delete the joke from the database
        db.session.commit()  # Commit the changes
        flash('Joke deleted successfully.', 'success')
    else:
        flash('Joke not found.', 'danger')

    return redirect(url_for('admin'))  # Redirect back to the admin page

@app.route('/admin/grant_admin_by_email', methods=['POST'])
@login_required
def grant_admin_by_email():
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('home'))

    email = request.form['email']
    user = User.query.filter_by(email=email).first()

    if user:
        user.role = 'admin'
        db.session.commit()
        flash(f'{user.email} has been granted admin rights.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('admin'))  # Redirect back to the admin panel


@app.route('/joke/like/<int:joke_id>', methods=['POST'])
@login_required
def like_joke(joke_id):
    joke = Joke.query.get_or_404(joke_id)
    # Logic to record the like in the database, e.g. incrementing the joke's rating
    joke.rating += 1  # Assuming rating is a numeric value
    db.session.commit()
    flash('You liked the joke!', 'success')
    return redirect(url_for('home'))

@app.route('/joke/dislike/<int:joke_id>', methods=['POST'])
@login_required
def dislike_joke(joke_id):
    joke = Joke.query.get_or_404(joke_id)
    # Logic to record the dislike in the database, e.g. decrementing the joke's rating
    joke.rating -= 1  # Assuming rating is a numeric value
    db.session.commit()
    flash('You disliked the joke!', 'warning')
    return redirect(url_for('home'))


@app.route('/admin/approve/<int:joke_id>', methods=['POST'])
@login_required
def approve_joke(joke_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('home'))

    joke = Joke.query.get(joke_id)
    if joke:
        joke.approved = True  # Set approved to True
        db.session.commit()
        flash('Joke approved successfully.', 'success')
    else:
        flash('Joke not found.', 'danger')

    return redirect(url_for('admin'))

@app.route('/admin/disapprove/<int:joke_id>', methods=['POST'])
@login_required
def disapprove_joke(joke_id):
    if current_user.role != 'admin':
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('home'))

    joke = Joke.query.get(joke_id)
    if joke:
        joke.approved = False  # Set approved to False
        db.session.commit()
        flash('Joke disapproved successfully.', 'success')
    else:
        flash('Joke not found.', 'danger')

    return redirect(url_for('admin'))
### Admin stuff ends here

if __name__ == '__main__':
    app.run(debug=True)