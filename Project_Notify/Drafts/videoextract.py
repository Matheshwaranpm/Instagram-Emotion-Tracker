import cv2
import numpy as np
import pytesseract
import pandas as pd
from selenium import webdriver
from plyer import notification
import joblib
import pyautogui
import time

# Function to extract text from image using OCR
def extract_text_from_image(image, post_region):
    # Crop image to include only the post region
    post_image = image[post_region[1]:post_region[1]+post_region[3], post_region[0]:post_region[0]+post_region[2]]
    gray = cv2.cvtColor(post_image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

# Load the emotion classifier model
pipe_lr = joblib.load(open("emotion_classifier_pipe_lr.pkl", "rb"))

# Load CSV file containing words and emotions
df = pd.read_csv("emotion_dataset.csv")

# Function to predict emotions
def predict_emotions(text):
    # Tokenize the text
    tokens = text.split()
    # Check if any token matches the words in the CSV file
    emotion = None
    for token in tokens:
        if token.lower() in df['word'].values:
            emotion = df[df['word'].str.lower() == token.lower()]['emotion'].values[0]
            break
    return emotion

# Function to notify user of detected emotion
def notify_user(emotion):
    if emotion:
        emoji_icon = emotions_emoji_dict[emotion]
        emotion_message = f"Hey buddy, you are in {emotion} mood {emoji_icon}!"
        notification.notify(
            title="Emotion Alert",
            message=emotion_message,
            app_name="Instagram Emotion Classifier"
        )

# Function to continuously monitor Instagram
def monitor_instagram(driver, post_region):
    # Variable to track consecutive posts with the same emotion
    consecutive_same_emotion = 0
    
    # Main loop
    while True:
        try:
            # Capture screenshot of the post region
            screenshot_path = "post_screenshot.png"
            post_screenshot = pyautogui.screenshot(region=post_region)
            post_screenshot.save(screenshot_path)
            
            # Extract text from the post screenshot
            image = cv2.imread(screenshot_path)
            text = extract_text_from_image(image, post_region)
            
            # Predict emotions from the extracted text
            emotion = predict_emotions(text)
            
            # Check if emotion matches previous post
            if emotion == prev_emotion:
                consecutive_same_emotion += 1
            else:
                consecutive_same_emotion = 0
            
            # If same emotion detected in consecutive posts exceeding threshold, notify user
            if consecutive_same_emotion >= 3:
                notify_user(emotion)
                consecutive_same_emotion = 0
            
            # Update previous emotion
            prev_emotion = emotion
            
        except Exception as e:
            print("Error:", e)
            # Handle exceptions as needed
        
        # Wait for 5 seconds before capturing next screenshot
        time.sleep(5)

# Main function
def main():
    # Initialize Selenium webdriver
    driver = webdriver.Chrome()

    # URL of the Instagram web page
    url = "https://www.instagram.com/"

    # Open Instagram in a visible Chrome browser window for user interaction
    driver.get(url)
    print("Instagram is now open in a visible browser window. Please interact with the page.")

    # Wait for user interaction
    input("Press Enter when you're ready to start monitoring...")

    # Find the region containing Instagram posts
    post_region = pyautogui.locateOnScreen('post_region251.png')

    # Check if post region is found
    if post_region:
        # Monitor Instagram
        monitor_instagram(driver, post_region)
    
    # Close the browser
    driver.quit()

