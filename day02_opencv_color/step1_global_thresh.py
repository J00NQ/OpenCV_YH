import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt 

# 이미지 읽기 (그레이스케일)
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)
# — cv.imread('image.png', cv.IMREAD_GRAYSCALE)
# — 또는 노이즈 제거: cv.medianBlur(img, 5)

# 콜백 함수 (트랙바용 — 빈 함수)
def nothing(x):
    pass
# def nothing(x):
#     pass

# 창 생성 (namedWindow)
# img = np.zeros((300,512,3), np.uint8)
cv.namedWindow('image')

# 트랙바 생성
cv.createTrackbar('Thresh','image',127,255,nothing)
# — threshold (0~255, 초기값 127)
# rest,thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
# rest,thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
# — mode: 0=THRESH_BINARY, 1=THRESH_BINARY_INV
mode_name = 'Mode (0:BIN, 1:INV)'
cv.createTrackbar(mode_name, 'image', 0, 1, nothing)

# 반복문
while(1):
    # 트랙바 값 읽기 (getTrackbarPos)
    thr = cv.getTrackbarPos('Thresh','image')
    m = cv.getTrackbarPos(mode_name,'image')
    # 이진화 적용
    # — mode가 0이면 THRESH_BINARY, 1이면 THRESH_BINARY_INV
    if m == 0:
        rest, result = cv.threshold(img, thr, 255, cv.THRESH_BINARY)
    else:
        rest, result = cv.threshold(img, thr, 255, cv.THRESH_BINARY_INV)

    # 원본 | 이진화 결과 나란히 표시
    # — np.hstack([img, thresh]) 또는 np.hstack([img, result])
    combined_img = np.hstack([img, result])
    # 현재 임계값을 화면에 표시
    # — cv.putText(result, f'Thresh: {value}', ...)
    cv.putText(combined_img, f'Thresh: {thr}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
    cv.imshow('image', combined_img)
    # 'q' → 종료
    k = cv.waitKey(1)
    # 'q' → break
    if k == ord("q") & 0xFF:
        break
# 창 닫기
cv.destroyAllWindows()