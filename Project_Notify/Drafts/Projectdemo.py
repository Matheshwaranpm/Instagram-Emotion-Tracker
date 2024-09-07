import time
import cv2
import numpy as np
import pytesseract
import pandas as pd
from selenium import webdriver
from plyer import notification
import pickle
from datetime import datetime
import joblib

# Load CSV file containing words and corresponding emotions
csv_file_path = "emotion_dataset.csv"  # Replace with the path to your CSV file
data = pd.read_csv(csv_file_path, header=None, names=["Emotion", "Clean_Text"])

# Load the trained sentiment analysis model
model_path = "emotion_classifier_pipe_lr.pkl"  # Replace with the path to your trained model
model = joblib.load(model_path)

def analyze_sentiment(text):
    # Tokenize the text into words
    words = text.split()
    
    # Initialize emotion counts
    emotion_counts = {emotion: 0 for emotion in data["Emotion"].unique()}
    
    # Check each word in the text for its corresponding emotion
    for word in words:
        emotion_match = data[data["Clean_Text"] == word]["Emotion"].values
        if len(emotion_match) > 0:
            emotion = emotion_match[0]
            emotion_counts[emotion] += 1
    
    # Convert counts to percentages
    total_words = sum(emotion_counts.values())
    if total_words > 0:
        emotion_percentages = {emotion: count/total_words for emotion, count in emotion_counts.items()}
    else:
        emotion_percentages = {emotion: 0 for emotion in emotion_counts.keys()}
    
    # Predict sentiment using the trained model
    sentiment = model.predict([text])[0]

    #convert sentiment to a String
    sentiment_str = str(sentiment)
    
    return emotion_percentages, sentiment

# Example usage:
text_file_path = "extracted_text.txt"  # Replace with the path to your text file
with open(text_file_path, "r") as file:
    text = file.read()

emotion_percentages, sentiment = analyze_sentiment(text)
print("Predicted sentiment:", sentiment)

#emotions emoji directory
emotions_emoji_dict = {"anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "😄", "joy": "😂", "neutral": "😐", "sad": "😔", "sadness": "😔", "shame": "😳", "surprise": "😮"}

# Function to extract text from image using OCR
def extract_text_from_image(image): 
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

    #Check if text is None
    if text is None:
        return " "

    # Print the extracted text
    print(text)

# Save the extracted text to a text file
with open('extracted_text.txt', 'w') as file:
    file.write(text)


# Initialize Selenium webdriver
driver = webdriver.Chrome()

# URL of the Instagram web page
url = "https://www.instagram.com/"

# Open Instagram in a visible Chrome browser window for user interaction
driver.get(url)
print("Instagram is now open in a visible browser window. Please interact with the page.")
input("Press Enter to start analyzing the screen...")

# Track previous content
previous_content = ""
previous_emotion = ""

# Track unique content and their count
unique_content_count = {}

# Main loop
while True:
    try:
        screenshot_path = "screenshot.png"
        for i in range(60):  # Capture screenshot every 1 second for 60 seconds
            time.sleep(5)
            driver.save_screenshot(screenshot_path)
            
            # Extract text from the screenshot
            image = cv2.imread(screenshot_path)
            text = extract_text_from_image(image)
            
            # Predict emotions from the extracted text
            emotion_percentages, predicted_sentiment = analyze_sentiment(text)
            
            # Compare with previous content and emotion
            if text != previous_content or predicted_sentiment != previous_sentiment:
                if (text, predicted_sentiment) in unique_content_count:
                    unique_content_count[(text, predicted_sentiment)] += 1
                else:
                    unique_content_count[(text, predicted_sentiment)] = 1
            
            # Update previous content and emotion
            previous_content = text
            previous_sentiment = predicted_sentiment
        
        # Check if any unique content occurs more than 3 times
        for content, count in unique_content_count.items():
            if count > 3:
                text, emotion = content
                # Display notification with the predicted emotion
                emoji_icon = emotions_emoji_dict[emotion]
                emotion_message = f"Hey buddy, you are in {emotion} mood {emoji_icon}!"
                notification.notify(
                    title="Emotion Alert",
                    message=emotion_message,
                    app_name="Instagram Emotion Classifier"
                )
        
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