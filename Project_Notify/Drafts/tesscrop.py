import cv2
import pytesseract

# Load the image
image = cv2.imread('screenx.png')

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

# Print the extracted text
print(text)

# Save the extracted text to a text file
with open('extracted_text.txt', 'w') as file:
    file.write(text)

