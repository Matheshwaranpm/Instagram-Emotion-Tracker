import time
import cv2
import numpy as np
import pytesseract
import pandas as pd
from selenium import webdriver
from win10toast import ToastNotifier
from datetime import datetime
import joblib

# Load CSV file containing words and corresponding emotions
csv_file_path = "emotion_dataset.csv"  # Replace with the path to your CSV file
data = pd.read_csv(csv_file_path, header=None, names=["Emotion", "Clean_Text"])

# Load the trained sentiment analysis model
model_path = "emotion_classifier_pipe_lr.pkl"  # Replace with the path to your trained model
model = joblib.load(model_path)

# Emotions emoji directory
emotions_emoji_dict = {
    "anger": "😠",
    "disgust": "🤮",
    "fear": "😨😱",
    "happy": "😄",
    "joy": "😂",
    "neutral": "😐",
    "sad": "😔",
    "sadness": "😔",
    "shame": "😳",
    "surprise": "😮"
}

# Function to analyze sentiment of text
def analyze_sentiment(text):
    # Predict sentiment using the trained model
    sentiment = model.predict([text])[0]
    # Convert sentiment to a String
    sentiment_str = str(sentiment)
    return sentiment

# Function to extract text from image using OCR
def extract_text_from_image(image, previous_content):
    # Define the region of interest (ROI) coordinates
    x = 240  # starting x-coordinate
    y = 130  # starting y-coordinate
    width = 760  # width of the ROI
    height = 880  # height of the ROI

    # Crop the image to the ROI
    roi = image[y:y+height, x:x+width]

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Perform text extraction using Tesseract on the ROI
    text = pytesseract.image_to_string(gray_roi)

    # Check if text is None
    if text is None:
        return previous_content

    # Print the extracted text
    print(text)
    return text

# Initialize Selenium webdriver
driver = webdriver.Chrome()

# URL of the Instagram web page
url = "https://www.instagram.com/"

# Open Instagram in a visible Chrome browser window for user interaction
driver.get(url)
print("Instagram is now open in a visible browser window. Please interact with the page.")
input("Press Enter to start analyzing the screen...")

# Track previous content and emotion
previous_content = ""
previous_sentiment = ""

# Track unique content and their count
unique_content_emotion_count = {}

# Initialize ToastNotifier
toaster = ToastNotifier()

# Main loop
while True:
    try:
        current_url = driver.current_url
        
        # Check if the user is in the direct message page
        if "/direct/" in current_url:
            print("User is in the direct message page. Stopping process for privacy reasons.")
            time.sleep(10)  # Wait for 10 seconds before checking again
            continue  # Skip the rest of the loop and check again
        
        screenshot_path = "screenshot.png"
        for i in range(60):  # Capture screenshot every 1 second for 60 seconds
            time.sleep(5)
            
            # Check if the user is in the direct message page before capturing the screenshot
            current_url = driver.current_url
            if "/direct/" in current_url:
                print("User is in the direct message page. Stopping process for privacy reasons.")
                break
            
            driver.save_screenshot(screenshot_path)

            # Extract text from the screenshot
            image = cv2.imread(screenshot_path)
            text = extract_text_from_image(image, previous_content)

            # Analyze sentiment of the extracted text
            sentiment = analyze_sentiment(text)

            # Check if the same emotion occurs for different content
            if sentiment != previous_sentiment:
                if sentiment in unique_content_emotion_count:
                    unique_content_emotion_count[sentiment] += 1
                else:
                    unique_content_emotion_count[sentiment] = 1

                # Check if any emotion occurs more than 3 times
                for emotion, count in unique_content_emotion_count.items():
                    if count > 3:
                        # Display notification with the predicted emotion
                        emoji_icon = emotions_emoji_dict[emotion]
                        emotion_message = f"Hey buddy, you are in {emotion} mood {emoji_icon}!"
                        toaster.show_toast("Emotion Alert", emotion_message, duration=10)

                # Update previous emotion
                previous_sentiment = sentiment

    except Exception as e:
        print("Error:", e)
        # Handle exceptions as needed

    # Check if the user navigated away from the Instagram page
    current_url = driver.current_url
    if not current_url.startswith("https://www.instagram.com/"):
        # End the loop if user navigates away
        break

# Close the browser
driver.quit()