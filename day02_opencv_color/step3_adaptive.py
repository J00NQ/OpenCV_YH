import cv2 as cv
import numpy as np

# 이미지 읽기 (그레이스케일)
# — 조명 불균형이 있는 이미지 권장
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

# 콜백 함수
# def nothing(x):
#     pass
def nothing(x):
    pass
# 창 생성
cv.imshow('image', img)

# 트랙바 생성
# — blockSize (3~31, 초기값 11, 반드시 홀수)
cv.createTrackbar('blockSize', 'image', 11, 31, nothing)
# — C (0~20, 초기값 2)
cv.createTrackbar('C', 'image', 2, 20, nothing)

# 반복문
while(1):
    # 트랙바 값 읽기
    block = cv.getTrackbarPos('blockSize', 'image')
    C = cv.getTrackbarPos('C', 'image') # C 값 읽어오기 추가
    # blockSize가 짝수면 1 더하기 (홀수 보장)
    # — if blockSize % 2 == 0: blockSize += 1
    if block < 3:
        block = 3
    if block % 2 == 0:
        block += 1
    # Global Threshold (고정)
    # — cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    ret1, global_th = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    # Otsu 자동 이진화
    # — cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    ret2, otsu_th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # Adaptive Mean Threshold
    # — cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C,
    #                        cv.THRESH_BINARY, blockSize, C)
    mean_th = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, block, C)
    # Adaptive Gaussian Threshold
    # — cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                        cv.THRESH_BINARY, blockSize, C)
    gaussian_th = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, block, C)
    # 2x2 격자로 표시
    # — top = np.hstack([global_th, otsu_th])
    # — bottom = np.hstack([mean_th, gaussian_th])
    # — result = np.vstack([top, bottom])
    top = np.hstack([global_th, otsu_th])
    bottom = np.hstack([mean_th, gaussian_th])
    result = np.vstack([top, bottom])
    cv.imshow('image', result)
    # 'q' → 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# 창 닫기
cv.destroyAllWindows()