import smtplib
import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the secret variables from the .env file
load_dotenv()

def send_email():
    # 1. Grab what the user typed into the UI boxes
    display_name = name_entry.get()
    recipient_email = email_entry.get()
    subject = subject_entry.get()
    # "1.0" means start at line 1, character 0. tk.END means go to the end.
    body = body_text.get("1.0", tk.END).strip()

    # 2. Check if the important fields are empty
    if not recipient_email or not subject or not body:
        messagebox.showwarning("Missing Info", "Please fill out all fields!")
        return

    # 3. Get your personal details safely from the hidden .env file
    sender_email = os.getenv("MY_EMAIL")
    sender_password = os.getenv("MY_APP_PASSWORD")

    if not sender_email or not sender_password:
        messagebox.showerror("Security Error", "Could not find .env file or credentials.")
        return

    # 4. Setup the MIME message
    msg = MIMEMultipart()
    msg['From'] = f"{display_name} <{sender_email}>" 
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # 5. Connect and Send
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        # 6. Show success popup and clear the text boxes
        messagebox.showinfo("Success", "Email sent successfully!")
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        body_text.delete("1.0", tk.END)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# --- User Interface (UI) Setup ---

# Create the main window
root = tk.Tk()
root.title("My Email Portal")
root.geometry("400x450") # Width x Height

# 1. Display Name Field
tk.Label(root, text="Display Name:").pack(pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.pack()

# 2. Recipient Email Field
tk.Label(root, text="Recipient Email Address:").pack(pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.pack()

# 3. Subject Field
tk.Label(root, text="Subject:").pack(pady=5)
subject_entry = tk.Entry(root, width=40)
subject_entry.pack()

# 4. Body Field (Made larger for multi-line text)
tk.Label(root, text="Body:").pack(pady=5)
body_text = tk.Text(root, width=40, height=10)
body_text.pack()

# 5. Send Button
send_button = tk.Button(root, text="Send Email", command=send_email, bg="lightblue", font=("Arial", 10, "bold"))
send_button.pack(pady=20)

# Run the UI loop
if __name__ == "__main__":
    root.mainloop()
