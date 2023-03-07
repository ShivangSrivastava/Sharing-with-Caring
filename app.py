from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
from flask_login import login_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# databased
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    ride_preference = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()

# other function

def get_gravatar(email):
    hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    return f'https://www.gravatar.com/avatar/{hash}?s=200&d=identicon'

# routing

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/login')
def login():
    return render_template('./auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['full-name']
        username = request.form['username']
        email = request.form['email']
        ride_preference = request.form['ride-preference']
        photo = get_gravatar(email)
        if not (User.query.filter_by(email=email).first()) and not (User.query.filter_by(username=username).first()):
            user = User(full_name=full_name, username=username, email=email, ride_preference=ride_preference, photo=photo)
            db.session.add(user)
        db.session.commit()

        return redirect('/dashboard')
    return render_template('./auth/signup.html')

@app.route('/reset')
def reset():
    return render_template('./auth/reset.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/index.html')

@app.route('/dashboard/profile')
@login_required
def profile():
    return render_template('dashboard/profile.html')

@app.route('/dashboard/about')
@login_required
def about():
    return render_template('dashboard/about.html')

@app.route('/dashboard/contact')
@login_required
def contact():
    return render_template('dashboard/contact.html')

@app.route('/dashboard/logout')
@login_required
def logout():
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