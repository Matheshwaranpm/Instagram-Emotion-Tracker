import pandas as pd
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
    
    return emotion_percentages, sentiment

# Example usage:
text_file_path = "extracted_text.txt"  # Replace with the path to your text file
with open(text_file_path, "r") as file:
    text = file.read()

emotion_percentages, sentiment = analyze_sentiment(text)
print("Predicted sentiment:", sentiment)