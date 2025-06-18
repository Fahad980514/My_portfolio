from flask_bootstrap import Bootstrap5
from flask import Flask, abort, render_template, redirect, url_for, flash, request
import os
from dotenv import load_dotenv, find_dotenv
import smtplib
from email.mime.text import MIMEText

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
eemail = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


app = Flask(__name__)
app.secret_key = os.getenv("app_key")
bootstrap = Bootstrap5(app)
print("Current directory:", os.getcwd())

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        subject = f"New Contact Form Submission from {name}"
        body = f"""
                You received a new message from your portfolio website contact form:

                Name: {name}
                Email: {email}
                Phone: {phone}
                Message:
                {message}
                """

        send_email(subject, body)

        flash("Your message has been sent successfully!")
        return redirect(url_for('home'))
    return render_template('index.html')

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = eemail
    msg['To'] = eemail

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(eemail, password)
            smtp.send_message(msg)
    except Exception as e:
        print("Email failed:", e)

if __name__ == '__main__':
    app.run(debug=True)