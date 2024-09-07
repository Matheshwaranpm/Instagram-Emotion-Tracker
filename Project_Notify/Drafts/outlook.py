import pytesseract
import PIL.Image
import cv2
import datetime
import os
from random import choice
from PIL import Image
import csv

#file selection

def my_function():
    
    folder_path = r"C:\Users\vishn\Project_Notify"

    image_files = [file for file in os.listdir(folder_path)
               if file.endswith((".jpg",".jpeg",".png"))]

    chosen_image = choice(image_files)

    image_path = os.path.join(folder_path,chosen_image)
    image = Image.open(image_path)
    image.show()

    #file tesseract process

    myconfig = r"--psm 6 --oem 3"

    text = pytesseract.image_to_string((image), config=myconfig)
    print(text)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M&S")
    file_name =f"result_{timestamp}.txt"

    with open("file_name","w") as file:
       file.write(text)

    #file analysing
    
    def read_text_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words = text.split()
            return set(words)

    def read_csv_file(file_path):
        words = set()
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                for word in row:
                    words.add(word)
        return words

    def find_common_words(text_file_path, csv_file_path):
        text_words = read_text_file(text_file_path)
        csv_words = read_csv_file(csv_file_path)
    
        common_words = text_words.intersection(csv_words)
    
        return common_words

    text_file_path = 'C:\\Users\\vishn\\Project_Notify\\file_name'
    csv_file_path = 'C:\\Users\\vishn\\Project_Notify\\sadwords.csv'

    common_words = find_common_words(text_file_path, csv_file_path)

    print("Common words found:")
    for word in common_words:
        print(word)

for _ in range(5):
    my_function()                 