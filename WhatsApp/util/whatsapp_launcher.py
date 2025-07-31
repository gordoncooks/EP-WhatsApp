import webbrowser
import time
import tkinter as tk
from tkinter import messagebox

def wait_for_whatsapp_login():
    # Open WhatsApp Web in the default browser
    webbrowser.open("https://web.whatsapp.com")
    print("Opening WhatsApp Web...")

    root = tk.Tk()
    root.withdraw()  # Hide main window

    while True:
        time.sleep(5)  # Wait 5 seconds before asking
        response = messagebox.askyesno("WhatsApp Login", "Have you signed in to WhatsApp Web?")
        if response:
            print("User confirmed WhatsApp is signed in. Starting automation...")
            break
        else:
            print("Waiting for user to sign in...")

if __name__ == "__main__":
    wait_for_whatsapp_login()
