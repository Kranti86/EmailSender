import smtplib
import os
from dotenv import load_dotenv # This imports the tool to read your .env file
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the secret variables from the .env file
load_dotenv()

def send_secure_email():
    # 1. Get your personal details securely from the .env file
    # We no longer need to use input() for these!
    sender_email = os.getenv("MY_EMAIL")
    sender_password = os.getenv("MY_APP_PASSWORD")
    
    # We still use input() for the things that change every time
    display_name = input("Enter the Sender Name (e.g., Homework Bot): ")
    recipient_email = input("Enter the recipient's email: ")
    subject = input("Enter the subject: ")
    body = input("Enter your message: ")

    # 2. Setup the MIME message
    msg = MIMEMultipart()
    msg['From'] = f"{display_name} <{sender_email}>" 
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # 3. Connect using SSL on Port 465
        print("Connecting to server...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        
        # 4. Login and Send
        print("Logging in...")
        server.login(sender_email, sender_password)
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("\nSuccess: Email sent!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    send_secure_email()
