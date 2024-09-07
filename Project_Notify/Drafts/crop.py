from PIL import Image

# Load the image
image = Image.open('screenx.png')

# Define the measurements for cropping
x = 240  # starting x-coordinate
y = 130  # starting y-coordinate
width = 760  # width of the crop
height = 880  # height of the crop

# Crop the image based on the measurements
cropped_image = image.crop((x, y, x + width, y + height))

# Save the cropped image
cropped_image.save('cropped_image.png')