import os
import requests
import tempfile
import pyperclip
from pynput import keyboard
from PIL import ImageGrab
from colorama import Fore, Style
import time

# Function to capture a screenshot with specific resolution and upload to Discord
def upload_to_discord():
    # Capture screenshot without compression
    screenshot = ImageGrab.grab()
    
    # Resize the screenshot to 1366x768
    screenshot = screenshot.resize((1366, 768))
    
    file_path = os.path.join(tempfile.gettempdir(), "screenshot.png")
    screenshot.save(file_path, quality=100)  # Save the resized screenshot with maximum quality
    
    webhook_url = 'YOUR_DISCORD_WEBHOOK'
    files = {'file': open(file_path, 'rb')}
    response = requests.post(webhook_url, files=files)
    
    if response.status_code == 200:
        print(Fore.GREEN + "Successfully uploaded screenshot to Discord." + Style.RESET_ALL)
        image_url = response.json()['attachments'][0]['url']
        pyperclip.copy(image_url)  # Copy the image URL to clipboard
    else:
        print(Fore.RED + "Failed to upload screenshot to Discord." + Style.RESET_ALL)

# Function to listen for "Print Screen" key press
def on_press(key):
    if key == keyboard.Key.print_screen:
        upload_to_discord()

# Start listening for key press
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
