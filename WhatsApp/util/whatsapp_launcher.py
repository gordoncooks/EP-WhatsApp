import time
import random
import pyautogui
import tkinter as tk
from tkinter import messagebox
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip


# =========================
# Helper Functions
# =========================

def wait_for_whatsapp_login():
    """Launch WhatsApp Web in Selenium using bundled Chrome + Chromedriver, wait for user login."""
    import os
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

    # Paths relative to the exe folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(base_dir, "chromedriver.exe")
    chrome_path = os.path.join(base_dir, "chrome-portable", "chrome.exe")

    # Configure Chrome options
    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    # Start Chrome using bundled driver and portable Chrome
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")
    print("Opening WhatsApp Web in bundled portable Chrome...")

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

    pyautogui.click()  # Focus window
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
    """Replace placeholders in the template with actual row values and log for debugging."""
    import pandas as pd

    def safe_int(value, col_name):
        """Convert value to int safely, handling strings, NaNs, and spaces."""
        if pd.isna(value):
            print(f"[DEBUG] {col_name} is NaN, treating as 0")
            return 0
        try:
            cleaned = str(value).replace(" ", "").replace(",", "")
            print(f"[DEBUG] {col_name} raw='{value}' cleaned='{cleaned}'")
            return int(cleaned)
        except ValueError:
            print(f"[DEBUG] {col_name} value='{value}' could not convert, treating as 0")
            return 0

    # Calculate total enquiries by summing relevant columns
    total_enquiries = (
        safe_int(row.get("All Contact Form (SMS)", 0), "All Contact Form (SMS)")
        + safe_int(row.get("All Number Viewed", 0), "All Number Viewed")
        + safe_int(row.get("All Email Viewed", 0), "All Email Viewed")
    )
    print(f"[DEBUG] Calculated total_enquiries = {total_enquiries} for row {row.get('Street Address_x', '[No Address]')}")

    # get name of the contact
    name = str(row.get("Owner Name", "")).strip()

    # make name title case
    name = name.title()
    name_parts = name.split(" ")
    name = name_parts[0]

    price_val = row.get("Price", 0)

    # Convert to numeric safely
    try:
        price_num = float(str(price_val).replace("R", "").replace(" ", "").replace("\u00A0", ""))
    except ValueError:
        price_num = 0

    # Format as South African currency with non-breaking spaces
    price = "R {:,.0f}".format(price_num).replace(",", "\u00A0")

    replacements = {
        "{name}": str(name),
        "{address}": str(row.get("Street Address_x", "[address]")),
        "{price}": str(price),
        "{views}": str(row.get("All Views", "[views]")),
        "{market_days}": str(row.get("Time On Market", "[market_days]")),
        "{enquiries}": str(total_enquiries),
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

            # Step 1: Open new chat
            open_new_chat_shortcut()
            time.sleep(2)

            # Step 2: Type phone number
            type_like_human(number)
            time.sleep(2)
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
