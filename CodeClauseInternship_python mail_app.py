import tkinter as tk
from tkinter import messagebox
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize database
def init_db():
    conn = sqlite3.connect('mail_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 password TEXT NOT NULL,
                 smtp_server TEXT NOT NULL,
                 smtp_port INTEGER NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS emails (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 sender TEXT NOT NULL,
                 recipient TEXT NOT NULL,
                 subject TEXT NOT NULL,
                 body TEXT NOT NULL)''')
    conn.commit()
    conn.close()

class MailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail Application")
        self.root.geometry("400x400")

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.smtp_server = tk.StringVar()
        self.smtp_port = tk.StringVar()
        self.recipient = tk.StringVar()
        self.subject = tk.StringVar()
        self.body = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Username:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.username).pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.password, show="*").pack(pady=5)

        tk.Label(self.root, text="SMTP Server:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.smtp_server).pack(pady=5)
        
        tk.Label(self.root, text="SMTP Port:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.smtp_port).pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        if not self.username.get() or not self.password.get() or not self.smtp_server.get() or not self.smtp_port.get():
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            conn = sqlite3.connect('mail_app.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, smtp_server, smtp_port) VALUES (?, ?, ?, ?)',
                      (self.username.get(), self.password.get(), self.smtp_server.get(), self.smtp_port.get()))
            conn.commit()
            conn.close()
            self.show_mail_frame()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_mail_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Recipient:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.recipient).pack(pady=5)

        tk.Label(self.root, text="Subject:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.subject).pack(pady=5)

        tk.Label(self.root, text="Body:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.body).pack(pady=5)

        tk.Button(self.root, text="Send Email", command=self.send_email).pack(pady=10)

    def send_email(self):
        if not self.recipient.get() or not self.subject.get() or not self.body.get():
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        try:
            conn = sqlite3.connect('mail_app.db')
            c = conn.cursor()
            c.execute('SELECT * FROM users ORDER BY id DESC LIMIT 1')
            user = c.fetchone()
            conn.close()

            msg = MIMEMultipart()
            msg['From'] = user[1]
            msg['To'] = self.recipient.get()
            msg['Subject'] = self.subject.get()
            msg.attach(MIMEText(self.body.get(), 'plain'))

            server = smtplib.SMTP(user[3], user[4])
            server.starttls()
            server.login(user[1], user[2])
            server.sendmail(user[1], self.recipient.get(), msg.as_string())
            server.quit()

            conn = sqlite3.connect('mail_app.db')
            c = conn.cursor()
            c.execute('INSERT INTO emails (sender, recipient, subject, body) VALUES (?, ?, ?, ?)',
                      (user[1], self.recipient.get(), self.subject.get(), self.body.get()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Email sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = MailApp(root)
    root.mainloop()
