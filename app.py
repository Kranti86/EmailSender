import smtplib
import os
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the secret variables from the .env file
load_dotenv()

# Setup the Flask Web App
app = Flask(__name__)
# A secret key is required for Flask to show popup messages (flashing) safely
app.secret_key = "homework_secret_key_change_me" 

@app.route("/", methods=["GET", "POST"])
def home():
    # If the user clicks the "Send Email" button (POST request)
    if request.method == "POST":
        # 1. Grab what the user typed into the HTML form
        display_name = request.form.get("display_name")
        recipient_email = request.form.get("recipient_email")
        subject = request.form.get("subject")
        body = request.form.get("body")

        # 2. Get your personal details safely from the hidden .env file
        sender_email = os.getenv("MY_EMAIL")
        sender_password = os.getenv("MY_APP_PASSWORD")

        if not sender_email or not sender_password:
            flash("Security Error: Could not find .env file.", "error")
            return render_template("index.html")

        # 3. Setup the MIME message
        msg = MIMEMultipart()
        msg['From'] = f"{display_name} <{sender_email}>" 
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # 4. Connect and Send
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            # Show success message on the webpage
            flash("Email sent successfully!", "success")
        except Exception as e:
            # Show error message on the webpage
            flash(f"An error occurred: {e}", "error")

    # If the user is just visiting the page (GET request), show the HTML form
    return render_template("index.html")

if __name__ == "__main__":
    # Run the web server
    app.run(debug=True)
