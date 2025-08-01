import time
import random
import pyautogui
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip


# =========================
# Helper Functions
# =========================

def wait_for_whatsapp_login():
    """Launch WhatsApp Web in Selenium and wait for user login."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://web.whatsapp.com")
    print("Opening WhatsApp Web...")

    # Popup to confirm login
    root = tk.Tk()
    root.withdraw()
    while True:
        time.sleep(5)
        if messagebox.askyesno("WhatsApp Login", "Have you signed in to WhatsApp Web?"):
            print("User confirmed WhatsApp login.")
            break
        else:
            print("Waiting for user to sign in...")

    # Click window to focus
    pyautogui.click()
    return driver


def type_like_human(text, min_delay=0.01, max_delay=0.03):
    """Type text character by character with human-like delays, using Shift+Enter for line breaks."""
    for char in text:
        if char == "\n":
            # Soft enter (line break without sending)
            pyautogui.keyDown('shift')
            pyautogui.press('enter')
            pyautogui.keyUp('shift')
        else:
            pyautogui.write(char)
        time.sleep(random.uniform(min_delay, max_delay))

    print(f"Finished human-like typing of message with soft line breaks.")

def copy_past_like_human(text, min_delay=0.01, max_delay=0.03):
    """
    Simulates human-like typing by copying text to clipboard and pasting it.
    Keeps the same method name for compatibility.
    """
    # Copy the text to clipboard
    pyperclip.copy(text)

    # Random small delay before pasting to mimic human behavior
    time.sleep(random.uniform(min_delay, max_delay))

    # Paste (Ctrl+V)
    pyautogui.hotkey('ctrl', 'v')

    # Optional delay after paste to simulate thinking time
    time.sleep(random.uniform(min_delay, max_delay))

    print(f"Pasted message via clipboard: {text[:30]}{'...' if len(text) > 30 else ''}")


def open_new_chat_shortcut(delay=0.1):
    """Simulate pressing Ctrl+Alt+N to open new chat."""
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('alt')
    pyautogui.keyDown('n')
    time.sleep(delay)
    pyautogui.keyUp('n')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('ctrl')
    print("Opened new chat (Ctrl+Alt+N).")


def fill_message_template(template, row):
    """Replace placeholders in the template with actual row values."""
    replacements = {
        "{name}": str(row.get("Owner Name", "[name]")),
        "{address}": str(row.get("Street Address_x", "[address]")),
        "{price}": str(row.get("Price", "[price]")),
        "{views}": str(row.get("All Views", "[views]")),
        "{market_days}": str(row.get("Time On Market", "[market_days]")),
        "{enquiries}": "0",
        "{hyperlink}": str(row.get("Extracted Hyperlink", "[hyperlink]")),
    }

    for tag, value in replacements.items():
        template = template.replace(tag, value)
    return template


# =========================
# Main Sending Function
# =========================

def start_whatsapp_sending(merged_df, template):
    """Automates WhatsApp message sending using pyautogui + Selenium."""
    if merged_df is None or merged_df.empty:
        print("No data to send.")
        return False

    driver = wait_for_whatsapp_login()

    time.sleep(10)  # Allow time for WhatsApp Web to load

    try:
        for idx, row in merged_df.iterrows():
            number = str(row.get("Owner Contact Numbers", "")).strip()

            # remove spaces, dashes, dots, and parentheses
            number = number.replace(" ", "").replace("-", "").replace(".", "").replace("(", "").replace(")", "")

            if number.startswith("0"):
                number = "+27" + number[1:] # Convert local number to international format

            if not number:
                print(f"Skipping row {idx}: No contact number")
                continue

            if number == "nan":
                print(f"Skipping row {idx}: Contact number is NaN")
                continue

            # get name of the contact
            name = str(row.get("Owner Name", "")).strip()

            # make name title case
            name = name.title()
            name_parts = name.split(" ")
            name = name_parts[0]

            # Step 1: Open new chat
            open_new_chat_shortcut()
            time.sleep(2)

            # Step 2: Type phone number
            type_like_human(number)
            time.sleep(1)
            pyautogui.press('enter')  # Open chat
            print(f"Opened chat with {number}")

            # Step 3: Wait for chat to load
            time.sleep(2)

            # Step 4: Fill and send message
            personalized_msg = fill_message_template(template, row)
            copy_past_like_human(personalized_msg)
            time.sleep(7)
            pyautogui.press('enter')
            print(f"Sent message to {number}")

            # Step 5: Small delay before next contact
            time.sleep(random.uniform(2, 4))

        print("All messages sent successfully.")
        driver.quit()
        return True

    except Exception as e:
        print(f"Error during WhatsApp sending: {e}")
        driver.quit()
        return False
