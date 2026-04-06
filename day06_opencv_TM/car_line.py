import cv2 as cv
import numpy as np

# 1단계: 이미지 로드
img = cv.imread('road.png')
#print(f"원본 이미지 크기 :{img.shape}") # 실제 크기 확인 

print(f"축소된 이미지 크기 :{img.shape}") # 실제 크기 확인 
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 2단계: Canny 에지 검출 (day04.md 참고)
edges = cv.Canny(gray, 100, 200, apertureSize=3)

# 3단계: 허프 직선 변환
lines = cv.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=100, maxLineGap=10)

# 4단계: 검출된 직선을 원본 이미지에 그리기
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv.imshow('Original', gray)
cv.imshow('Edges', edges)
cv.imshow('Hough Lines', img)
cv.waitKey(0)
cv.destroyAllWindows()