import cv2 as cv
import numpy as np

# 이미지 읽기 (그레이스케일)
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

# 창 생성
cv.imshow('image', img)

# 트랙바 생성
def nothing(x):
    pass

# manual_thresh (0~255, 초기값 127)
cv.createTrackbar('Manual_thresh', 'image', 127, 255, nothing)

# mode: 0=Otsu만, 1=수동+Otsu 비교
mode = '0:Otsu, 1:manual+Otsu'
cv.createTrackbar(mode, 'image', 0, 1, nothing)

# 반복문
while(1):
    manual_thresh = cv.getTrackbarPos('Manual_thresh', 'image')
    m = cv.getTrackbarPos(mode, 'image')

    # 수동 이진화
    ret_manual, manual_th = cv.threshold(img, manual_thresh, 255, cv.THRESH_BINARY)

    # Otsu 자동 이진화
    ret_otsu, otsu_th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # 텍스트 표시용 복사
    img_cp = img.copy()
    cv.putText(img_cp, f'Thresh: {manual_thresh}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

    # Otsu 임계값 표시
    cv.putText(otsu_th, f'Otsu: {ret_otsu:.0f}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, 255, 2)

    # 결과 합치기
    if m == 0:
        # 원본 | Otsu
        result = np.hstack((img_cp, otsu_th))
    elif m == 1:
        # 원본 | 수동 | Otsu
        result = np.hstack((img_cp, manual_th, otsu_th))

    cv.imshow('image', result)

    # 'q' → 종료
    k = cv.waitKey(1)
    if k == ord("q") & 0xFF:
        break

# 창 닫기
cv.destroyAllWindows()