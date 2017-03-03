import cv2
import sys
from test import drawcontour_
#from Video_CharsRecognizer import drawcontour_
import numpy as np


video_capture = cv2.VideoCapture('video1.mp4')
#video_capture = cv2.VideoCapture(0)
from LetterRecognizer import recognizer_forContourRecognizer
predictor = recognizer_forContourRecognizer.init()

while True:
    ret, frame = video_capture.read()

    drawcontour_(frame, predictor)
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.imshow('video',frame)
    #cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()