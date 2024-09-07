import cv2
import pytesseract

video = cv2.VideoCapture("videosample.mp4")

while video.isOpened():
    ret, frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)
    print (text)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    video.release()
    cv2.destroyAllWindows()