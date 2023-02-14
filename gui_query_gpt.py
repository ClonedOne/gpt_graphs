"""
Written for the m1 macbook pro 14"
"""

import os
import json
import time
import random
import pyperclip
import pyautogui

print(pyautogui.size())
query_dir = "queries"
resp_dir = "responses"


def new_chat():
    """Open new chat tab"""
    pyautogui.moveTo(100, 150, duration=random.uniform(0.5, 1.5))
    # Focus on window
    pyautogui.click()
    time.sleep(1)
    # Click new chat
    pyautogui.click()


def type_query(query):
    """Type query into input field"""
    pyautogui.moveTo(700, 1100, duration=random.uniform(0.5, 1.5))
    # Focus on window
    pyautogui.click()
    time.sleep(1)
    # Focus on input field
    pyautogui.click()
    pyautogui.typewrite(query, interval=random.uniform(0.05, 0.1))
    # press enter
    pyautogui.press("enter")


def capture_screen_text():
    """Use CTRL-A + copy to select and copy all text on screen"""
    pyautogui.moveTo(1500, 600, duration=random.uniform(0.5, 1.5))

    # Focus on window
    pyautogui.click()
    time.sleep(1)

    # Select all and copy
    pyautogui.hotkey("command", "a")
    pyautogui.hotkey("command", "c")
    time.sleep(1)

    # Get copied text as string
    text = pyperclip.paste()
    return text


def main():
    os.makedirs(resp_dir, exist_ok=True)

    # Iterate through the queries, in json files
    for query_file in os.listdir(query_dir):
        query = json.load(open(os.path.join(query_dir, query_file), "r"))["query"]

        # Open new chat tab
        new_chat()
        type_query(query)
        time.sleep(55)
        response = capture_screen_text()

        # Save response to file
        with open(os.path.join(resp_dir, query_file), "w") as f:
            f.write(response)

        # Wait for a randomized timeout explicitly
        timeout = random.randint(1, 10)
        time.sleep(timeout)


if __name__ == "__main__":
    main()
