from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/login')
def login():
    return render_template('./auth/login.html')

@app.route('/signup')
def signup():
    return render_template('./auth/signup.html')

@app.route('/reset')
def reset():
    return render_template('./auth/reset.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html')

@app.route('/dashboard/profile')
def profile():
    return render_template('dashboard/profile.html')

@app.route('/dashboard/about')
def about():
    return render_template('dashboard/about.html')

@app.route('/dashboard/contact')
def contact():
    return render_template('dashboard/contact.html')

@app.route('/dashboard/logout')
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