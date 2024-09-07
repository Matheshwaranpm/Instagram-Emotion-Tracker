import pytesseract
import PIL.Image
import cv2
import datetime

myconfig = r"--psm 11 --oem 3"

text = pytesseract.image_to_string(PIL.Image.open("screenshot.png"), config=myconfig)
print(text)

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M&S")
file_name =f"result_{timestamp}.txt"

with open("file_name","w") as file:
    file.write(text)