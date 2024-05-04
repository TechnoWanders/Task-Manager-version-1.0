from flask import Flask, render_template, url_for, redirect

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/signin_page')
def signin_page():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)