import smtplib
import os
from flask import Flask, render_template, request, flash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Explicitly map templates for Vercel routing
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
# Secret key is still required for the flash messages to work securely
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key_123")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # 1. Grab ALL data explicitly from your HTML form fields
        display_name = request.form.get("display_name")
        sender_email_input = request.form.get("sender_email")
        recipient_email = request.form.get("recipient_email")
        subject = request.form.get("subject")
        body = request.form.get("body")

        # 2. Get the authentication password from Vercel (Do NOT put this in UI for security)
        # Your sender_email_input MUST match the account this password belongs to
        sender_password = os.environ.get("MY_APP_PASSWORD")

        if not sender_password:
            flash("Server Configuration Error: Missing Application Password in Vercel environment.", "error")
            return render_template("index.html")

        # 3. Construct the Email exactly as inputted
        msg = MIMEMultipart()
        msg['From'] = f"{display_name} <{sender_email_input}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # 4. Connect and send via Gmail SMTP
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email_input, sender_password)
            server.send_message(msg)
            server.quit()
            flash("Message sent successfully!", "success")
        except smtplib.SMTPAuthenticationError:
            flash("Authentication Error: The password on Vercel does not match the Sender Email you typed.", "error")
        except Exception as e:
            flash(f"Transmission Error: {str(e)}", "error")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
