import cv2
import sys
#from test import drawcontour_
from Video_CharsRecognizer import drawcontour_
import numpy as np
import os


def load_allpath(path):
    res = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file[0] is '.':
                continue
            filepath = os.path.join(root, file)
            res.append(filepath)
    return res


from LetterRecognizer import recognizer_forContourRecognizer
predictor = recognizer_forContourRecognizer.init()

res = load_allpath("data")
for filepath in res:
    img = cv2.imread(filepath)
    #img = cropsize(img)

    draw_flag = drawcontour_(img, predictor)
    #if draw_flag:
        #print(filepath)
    cv2.namedWindow('video', cv2.WINDOW_FULLSCREEN)
    cv2.imshow('video',img)
    cv2.waitKey(0)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
#video_capture.release()
cv2.destroyAllWindows()