import numpy as np
import cv2
from matplotlib import pyplot as plt
from operator import itemgetter
import operator
import os.path




def drawcontour_(image, predictor):

    videoimg = image

#    if videoimg.shape[2] is 3:
    gray = cv2.cvtColor(videoimg, cv2.COLOR_BGR2GRAY)
    # imshow_(gray)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
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
                cv2.drawContours(videoimg, [approx], -1, (255, 0, 0), 1)
                #imshow_(videoimg)
                crop_img = videoimg[y-2:y + h+2, x-2:x + w+2]
                #imshow_(crop_img)

                result = Cropped_Licenseplate(crop_img, predictor)
                if len(result) > 0:
                    print(result)
                    return True


                #result=area
                #font = cv2.FONT_HERSHEY_SIMPLEX
                #cv2.putText(videoimg, result, (x, y + h + 20), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                #cv2.putText(videoimg, str(result), (x, y + h + 20), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                #cv2.waitKey(0)

        else:
            pass

    return False



def Cropped_Licenseplate(crop_img1, predictor):

    imgfile = crop_img1

    gray = cv2.GaussianBlur(imgfile, (3, 3), 0)
    # imshow_(blur)
    #ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # imshow_(thresh)
    edged = cv2.Canny(gray, 500, 150)
    # imshow_(edged)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # imshow_(closed)

    img2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    height, width, channels = imgfile.shape
    total_area = width * height
    appropriate_contours = find_appropriate_contours(contours, total_area)

    from erode_checker import find_independant_idx
    max_area_idxs = find_independant_idx(appropriate_contours)

    results = []
    for idx in max_area_idxs:
        result = puttext_below_contour(crop_img1, imgfile, appropriate_contours[idx], predictor)
        if result is not None:
            results.append(result)

    return(results)

def puttext_below_contour(crop_img1, imgfile, contour, predictor):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(imgfile, (x, y), (x + w, y + h), (0, 255, 0), 1)
    crop_img2 = imgfile[y - 2:y + h + 2, x - 2:x + w + 2]

    from LetterRecognizer.recognizer_forContourRecognizer import letter_recognizer_with_opencvimage
    crop_img2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

    result = None
    if crop_img2 is not None:
        result = letter_recognizer_with_opencvimage(crop_img2, predictor)[0]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(crop_img1, str(result), (x, y + h + 20), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    return result

def find_appropriate_contours(contours, total_area):
    appropriate_contours = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        aspectratio = float(w) / h
        pick_area = w * h
        #extent = float(pick_area) / total_area
        extent = float(area) / total_area

        #if 1.2 > (aspectratio) > 0.25 and (extent) > 0.02:
        if 1.2 > (aspectratio) > 0.01 and (extent) > 0.01:
            appropriate_contours.append(c)
    return appropriate_contours
