"""
Written for the m1 macbook pro 14"
Assumes Chromium browser is open and logged in to OpenAI's web interface
with a full screen window, not maximized.
All the magic numbers are based on this setup.
"""

import os
import time
import random
import argparse
import pyperclip
import pyautogui
from pathlib import Path


resp_dir = "responses"
error_msg = "An error occurred. If this issue persists please contact us through our help center at help.openai.com."


def new_chat():
    """Open new chat tab in the web interface"""
    pyautogui.moveTo(100, 150, duration=random.uniform(0.5, 1.5))
    # Focus on window
    pyautogui.click()
    time.sleep(1)
    # Click new chat
    pyautogui.click()


def type_query(query: str):
    """Type the query in the input field

    Args:
        query (str): query string
    """
    pyautogui.moveTo(700, 1120, duration=random.uniform(0.5, 1.5))
    # Focus on window
    pyautogui.click()
    time.sleep(1)
    # Focus on input field
    pyautogui.click()
    
    # Copy-paste instead of typing to avoid issues with newlines
    pyperclip.copy(query)
    pyautogui.hotkey("command", "v")
    time.sleep(random.uniform(0.2, 0.7))
    
    # press enter
    pyautogui.press("enter")


def capture_screen_text() -> str:
    """Use CTRL-A + copy to select and copy all text on screen

    Returns:
        str: text capture of the screen
    """
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


def process_query(query: str) -> str:
    # Open new chat tab
    new_chat()
    type_query(query)
    # Completion time can be long
    time.sleep(random.randint(40, 60))
    response = capture_screen_text()

    # Check for error message, if found raise exception
    if error_msg in response:
        raise Exception("Error with query: " + query)

    return response


def main(args: dict):
    # Dir management
    query_dir = args["query_dir"]
    experiment_query_dir = Path(query_dir).name
    resp_path = os.path.join(resp_dir, experiment_query_dir)
    os.makedirs(resp_path, exist_ok=True)

    # Iterate through the query files in the directory.
    # Each query file is a .txt file containing only a single query.
    for query_file in os.listdir(query_dir):
        with open(os.path.join(query_dir, query_file), "r") as f:
            query = f.read()
        print("Processing query: " + query)

        # Process query. If error, delay for a randomized timeout
        # and try again. Timeout should be at least a minute.
        response = None
        while response is None:
            try:
                response = process_query(query)
            except Exception:
                time.sleep(random.randint(60, 120))

        # Save response to file
        with open(os.path.join(resp_path, query_file), "w") as f:
            f.write(response)

        # Wait for a randomized timeout explicitly
        time.sleep(random.randint(5, 10))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query_dir", type=str, default="queries/test")
    arguments = parser.parse_args()
    main(vars(arguments))
