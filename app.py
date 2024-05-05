from flask import Flask, render_template, url_for, redirect, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import logging

app = Flask(__name__, static_folder='static')

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

otp_storage = None

@app.route('/send_otp', methods=['POST'])
def send_otp():
    if request.method =='POST':
        receiver_email = request.form['rec_email']
        otp = generate_otp()
        save_otp(otp)
        if send_email(receiver_email, otp):
            return 'OTP sent successfully!'
        else:
            return 'Failed to send OTP. Please try again.'

def save_otp(otp):
    global otp_storage 
    otp_storage = otp

def verify_otp_logic(otp):
        global otp_storage
        if (otp == otp_storage):
            return True
        else:
            return False


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        if verify_otp_logic(otp):
            return 'OTP verified successfully!'
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

@app.route('/otpvfcs')
def verify_page():
    return render_template('otpvfcs.html')

if __name__ == '__main__':
    app.run(debug=True)