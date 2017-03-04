import cv2
import sys
#from test import drawcontour_
from Video_CharsRecognizer import drawcontour_
import numpy as np
import os


video_dir = "data/mov"
video_filename = 'video1.mp4'
video_filename = 'KakaoTalk_Video_2017-03-03-14-41-55 (1).mp4'
video_filename = os.path.join(video_dir, video_filename)

alive_flag = False
if alive_flag:
    video_capture = cv2.VideoCapture(0)
else:
    video_capture = cv2.VideoCapture(video_filename)

from LetterRecognizer import recognizer_forContourRecognizer
predictor = recognizer_forContourRecognizer.init()

while True:
    ret, frame = video_capture.read()

    draw_flag = drawcontour_(frame, predictor)
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.imshow('video',frame)
    if draw_flag:
        cv2.waitKey(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()