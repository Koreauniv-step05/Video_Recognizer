import cv2
import sys
from erode_checker import find_independant_idx

video_capture = cv2.VideoCapture('video1.mp4')
while True:
    ret, frame = video_capture.read()

    videoimg = frame

    gray = cv2.cvtColor(videoimg, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    edged = cv2.Canny(gray, 300, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    img2, contours, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    max_area_idxs = find_independant_idx(contours)
    print(max_area_idxs)

    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()