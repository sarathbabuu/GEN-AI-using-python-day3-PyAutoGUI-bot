# daily_report_bot.py

import pyautogui
import pyperclip
import subprocess
import time
from datetime import datetime
import os

# -----------------------------
# Configuration
# -----------------------------

WEBSITE_URL = "https://weather.com"

SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Documents")

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0

# -----------------------------
# Helper Functions
# -----------------------------

def wait(seconds):
    time.sleep(seconds)


def open_chrome():
    """
    Opens Google Chrome.
    Windows example.
    Adjust path if needed.
    """
    try:
        subprocess.Popen(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
    except:
        # Fallback
        pyautogui.press("win")
        wait(1)
        pyautogui.write("chrome", interval=0.05)
        pyautogui.press("enter")

    wait(5)


def get_weather_information():
    """
    Navigates to weather.com and copies
    a visible piece of information.

    This example assumes the first visible
    temperature can be selected manually
    using keyboard navigation.

    In real deployment, image recognition
    should be used for better reliability.
    """

    pyautogui.hotkey("ctrl", "l")
    pyautogui.write(WEBSITE_URL, interval=0.03)
    pyautogui.press("enter")

    wait(8)

    # Select page text
    pyautogui.hotkey("ctrl", "a")
    wait(1)

    pyautogui.hotkey("ctrl", "c")
    wait(2)

    page_text = pyperclip.paste()

    fetched_info = "Weather information unavailable"

    # Simple extraction attempt
    if page_text.strip():
        fetched_info = page_text[:100]

    return fetched_info


def open_excel():
    """
    Opens Microsoft Excel.
    """

    pyautogui.press("win")
    wait(1)

    pyautogui.write("excel", interval=0.05)
    pyautogui.press("enter")

    wait(8)


def create_excel_entry(fetched_data):
    """
    Creates one row with:
    DateTime | Data | Comment
    """

    current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    comment = "Good for outdoor activities"

    # Fill columns A, B, C
    pyautogui.write(current_dt)
    pyautogui.press("tab")

    pyautogui.write(fetched_data[:100])
    pyautogui.press("tab")

    pyautogui.write(comment)

    return current_dt


def save_excel_file():
    """
    Saves workbook using today's date.
    """

    today = datetime.now().strftime("%Y-%m-%d")

    filename = f"daily_report_{today}.xlsx"

    pyautogui.hotkey("ctrl", "s")
    wait(3)

    full_path = os.path.join(SAVE_FOLDER, filename)

    pyautogui.write(full_path, interval=0.03)
    pyautogui.press("enter")

    wait(5)

    return filename


def capture_screenshot():
    """
    Captures final Excel sheet screenshot.
    """

    today = datetime.now().strftime("%Y-%m-%d")

    screenshot_name = os.path.join(
        SAVE_FOLDER,
        f"daily_report_{today}.png"
    )

    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_name)

    return screenshot_name


# -----------------------------
# Main Workflow
# -----------------------------

def main():

    print("Starting Daily Report Bot...")

    # Step 1 - Open Chrome
    open_chrome()

    # Step 2 - Fetch information
    fetched_data = get_weather_information()

    print("Fetched Data:")
    print(fetched_data)

    # Step 3 - Open Excel
    open_excel()

    # Step 4 - Add report row
    create_excel_entry(fetched_data)


    # Step 5 - Save Excel file
    excel_file = save_excel_file()

    # Step 6 - Screenshot
    screenshot_file = capture_screenshot()

    print(f"Excel saved: {excel_file}")
    print(f"Screenshot saved: {screenshot_file}")
    print("Daily Report Bot Completed.")


if __name__ == "__main__":
    main()