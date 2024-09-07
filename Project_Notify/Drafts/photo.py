import os
from random import choice
from PIL import Image

folder_path = r"C:\Users\vishn\Project_Notify"

image_files = [file for file in os.listdir(folder_path)
               if file.endswith((".jpg",".jpeg",".png"))]

chosen_image = choice(image_files)

image_path = os.path.join(folder_path,chosen_image)
image = Image.open(image_path)
image.show()