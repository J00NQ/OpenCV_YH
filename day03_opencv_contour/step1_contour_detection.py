import cv2 as cv
import numpy as np

# 이미지 로드 (그레이스케일)
iamge_path = './img/sudoku.png'
img = cv.imread(iamge_path)
# img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)
img2 = img.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 또는 임계값으로 이진화
# _, binary = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
ret, th = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

# 컨투어 검출
# contours, hierarchy = cv.findContours(binary, ..., ...)
contours, hierarchy = cv.findContours(th, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cntr = contours[0]
cv.drawContours(img, [cntr], -1, (0, 255, 0), 1)
# 칼라 이미지로 변환 (그리기용)
# img_color = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
img_color = cv.cvtColor(th, cv.COLOR_GRAY2BGR)

# 모든 컨투어 그리기
# cv.drawContours(img_color, contours, -1, (0, 255, 0), 2)
cv.drawContours(img_color, contours, -1, (0, 255, 0), 2)

# 면적 필터링 (100~5000 픽셀 범위)
# for cnt in contours:
#     area = cv.contourArea(cnt)
#     if 100 < area < 5000:
#         # 조건을 만족하는 컨투어를 파란색으로 그리기
#         cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 2)
for cnt in contours:
    area = cv.contourArea(cnt)
    if 100 < area < 10000:
        cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 2)

# 결과 표시
# cv.imshow('Filtered Contours', img_color)
# cv.waitKey(0)
# cv.destroyAllWindows()
cv.imshow('Filtered Contours', img_color)
cv.waitKey(0)
cv.destroyAllWindows()