import numpy as np
import cv2
from matplotlib import pyplot as plt
from operator import itemgetter
import operator
import os.path


def drawcontour_(image):

    videoimg = image

    gray = cv2.cvtColor(videoimg, cv2.COLOR_BGR2GRAY)
    # imshow_(gray)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    # imshow_(blur)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # imshow_(thresh)
    edged = cv2.Canny(gray, 300, 150)
    # imshow_(edged)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # imshow_(closed)

    img2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        aspectratio = float(w) / h
        height, width, channels = videoimg.shape
        pick_area = w * h
        total_area = width * height
        #extent = float(pick_area) / total_area
        extent = float(area) / total_area

        if (aspectratio) > 6:
            pass

        elif 6 > (aspectratio) > 1.6:
            if len(approx) == 4 and (extent) > 0.005:
                cv2.drawContours(videoimg, [approx], -1, (0, 255, 0), 3)
                #imshow_(videoimg)
                #crop_img = img[y-2:y + h+2, x-2:x + w+2]
                #imshow_(crop_img)


        else:
            pass

