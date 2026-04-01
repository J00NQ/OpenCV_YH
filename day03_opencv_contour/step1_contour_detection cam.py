import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("camera not found")
    exit()

cv.namedWindow('cam', cv.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cntr = contours[0]
        cv.drawContours(frame, [cntr], -1, (0, 255, 0), 1)
    img_color = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
    cv.drawContours(img_color, contours, -1, (0, 255, 0), 2)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if 100 < area < 10000:
            cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 2)
    binary_color = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
    result = np.hstack([binary_color, frame])
    cv.imshow('cam', result)
    cv.imshow('Filtered Contours', img_color)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.waitKey(0)
cap.release()
cv.destroyAllWindows()