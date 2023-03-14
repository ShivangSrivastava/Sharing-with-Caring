from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)


# database model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    ride_preference = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.username}>'



with app.app_context():
    db.create_all()

# user loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# other function

def get_gravatar(email):
    hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    return f'https://www.gravatar.com/avatar/{hash}?s=200&d=identicon'

# routing

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/dashboard')
        flash('Incorrect username or password.')
    return render_template('./auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full-name']
        username = request.form['username']
        email = request.form['email']
        ride_preference = request.form['ride-preference']
        password = request.form['password']
        photo = get_gravatar(email)
        if not (User.query.filter_by(email=email).first()) and not (User.query.filter_by(username=username).first()):
            user = User(full_name=full_name, username=username, email=email, ride_preference=ride_preference, password=password, photo=photo)
            db.session.add(user)
            db.session.commit()
            login_user(user) # automatically log in the new user
            return redirect('/dashboard')
        flash('Email or username already exists.')
    return render_template('./auth/signup.html')

@app.route('/reset')
def reset():
    return render_template('./auth/reset.html')


@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        # user is authenticated, show dashboard
        return render_template('./dashboard/index.html')
    else:
        # user is not authenticated, show login page
        return redirect('/login')

@app.route('/profile/<username>')
def user_profile(username):

    # Get the user ID from the session
    user_id = session.get('user_id')

    # Retrieve the user's profile data from the database using their username
    user = User.query.filter_by(username=username).first()
    username=user.username
    full_name=user.full_name
    email=user.email
    ride_preference = user.ride_preference
    photo=user.photo
    # Check if the user is authenticated and the profile belongs to the current user
    if user:
        return render_template('./profile.html',username=user.username,full_name=user.full_name,email=user.email,ride_preference = user.ride_preference,photo=user.photo)

    else:
        # Redirect the user to the login page
        flash('User not exist')
        return redirect('/')
    
@app.route('/dashboard/about')
@login_required
def about():
    return render_template('./dashboard/about.html')

@app.route('/dashboard/contact')
@login_required
def contact():
    return render_template('./dashboard/contact.html')


@app.route('/dashboard/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

if __name__ == "__main__":
    
    host="127.0.0.1"
    port=5000
    
    app.run(debug=True, host=host, port=port)