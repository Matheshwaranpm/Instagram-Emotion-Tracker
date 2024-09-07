import pytesseract
import PIL.Image
import cv2
import pandas as pd

def compare_words(dataframe,text):
    dataframe = set()
    text = set()

dataframe = pd.read_csv("C:\\Users\\vishn\\Project_Notify\\sadwords.csv")

myconfig = r"--psm 6 --oem 3"

text = pytesseract.image_to_string(PIL.Image.open("insta.jpg"), config=myconfig)

matching_words = list(dataframe.intersection(text))
print(matching_words)


    