from flask import Flask, session, render_template, url_for, redirect, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__, static_folder='static')
app.secret_key = 'notyourbusiness'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

def create_database():
    with app.app_context():
        db.create_all()

def is_valid_email(email):
    existing_email = User.query.filter_by(email=email).first()
    return existing_email is None

def is_available_username(username):
    existing_user = User.query.filter_by(username=username).first()
    return existing_user is None

@app.route('/create_account', methods=['POST'])
def create_account():
    create_database()
    email = request.form.get('reciever_email')
    username = request.form.get('username')
    password = request.form.get('password')

    if not is_valid_email(email):
        error_message = 'Email Address already taken'
        return render_template('signin.html', error_message = error_message)
    
    if not is_available_username(username):
        error_message = 'Username already taken'
        return render_template('signin.html',error_message = error_message)

    session['temp_email'] = email
    session['temp_username'] = username
    session['temp_password'] = password

    return render_template('otpvfcs0.html')

def generate_otp():
    return str(random.randint(100000, 999999))

# Send Email
def send_email(receiver_email, otp):
    sender_email = 'nipopipo14@gmail.com'
    sender_password = 'camh ocwk dzkc ibyf'  
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Your One-Time Password (OTP)'
    
    body = f'Your OTP is: {otp}'
    message.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


@app.route('/send_otp', methods=['POST'])
def send_otp():
    if request.method =='POST':
        receiver_email = request.form['rec_email']
        otp = generate_otp()
        session['otp'] = otp
        if send_email(receiver_email, otp):
            return render_template('otpvfcs.html')
        else:
            return 'Failed to send OTP. Please try again.'


def verify_otp_logic(entered_otp):
        otp = session.get('otp')
        if entered_otp == otp:
            return True
        else:
            return False

def insert(session, db, User):
    email = session.get('temp_email')
    username = session.get('temp_username')
    password = session.get('temp_password')
    print(email)

    new_user = User(email = email, username = username, password = password)
    db.session.add(new_user)
    db.session.commit()

    session.pop('temp_email', None)
    session.pop('temp_username', None)
    session.pop('temp_password', None)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if verify_otp_logic(entered_otp):
            insert()
            message = 'OTP verified successfully && Account created successfully'
            return render_template('tasksite.html', message = message)
        else:
            return 'Failed to verify OTP. Please try again.'
    return 'Invalid request.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/signin_page')
def signin_page():
    return render_template('signin.html')

@app.route('/view_database')
def database_interaction():
    users = User.query.all()
    #print(users.id)
    return render_template('dbinteract.html', users = users)

if __name__ == '__main__':
    app.run(debug=True)