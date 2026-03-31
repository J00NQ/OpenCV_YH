import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

def nothing(x):
    pass

def hsv_to_bgr(h, s, v):
    hsv = np.uint8([[[h, s, v]]])
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return bgr[0][0]

def create_hue_gradient(width=512, height=50):
    gradient = np.zeros((height, width, 3), np.uint8)
    for x in range(width):
        h = int(x * 179 / width)
        gradient[:, x] = (h, 255, 255)
    return cv.cvtColor(gradient, cv.COLOR_HSV2BGR)

cv.namedWindow('image')

# HSV trackbars
cv.createTrackbar('H_min','image',0,179,nothing)
cv.createTrackbar('S_min','image',0,255,nothing)
cv.createTrackbar('V_min','image',0,255,nothing)

cv.createTrackbar('H_max','image',179,179,nothing)
cv.createTrackbar('S_max','image',255,255,nothing)
cv.createTrackbar('V_max','image',255,255,nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. trackbar 값 읽기
    h_min = cv.getTrackbarPos('H_min','image')
    s_min = cv.getTrackbarPos('S_min','image')
    v_min = cv.getTrackbarPos('V_min','image')

    h_max = cv.getTrackbarPos('H_max','image')
    s_max = cv.getTrackbarPos('S_max','image')
    v_max = cv.getTrackbarPos('V_max','image')

    # ❗ S, V만 정렬 (Hue는 정렬하면 안됨)
    s_min, s_max = min(s_min, s_max), max(s_min, s_max)
    v_min, v_max = min(v_min, v_max), max(v_min, v_max)

    # 2. HSV 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 3. mask 생성 (wrap-around 처리)
    if h_min <= h_max:
        mask = cv.inRange(hsv, (h_min,s_min,v_min), (h_max,s_max,v_max))
    else:
        mask1 = cv.inRange(hsv, (0,s_min,v_min), (h_max,s_max,v_max))
        mask2 = cv.inRange(hsv, (h_min,s_min,v_min), (179,s_max,v_max))
        mask = mask1 | mask2

    # 4. 결과
    res = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    # -------------------------
    # ✔ 단색 preview
    color_min = hsv_to_bgr(h_min, s_min, v_min)
    color_max = hsv_to_bgr(h_max, s_max, v_max)

    preview = np.zeros((100, 512, 3), np.uint8)
    preview[:, :256] = color_min
    preview[:, 256:] = color_max

    cv.imshow('range_preview', preview)

    # -------------------------
    # ✔ Hue gradient + 선택 영역 표시
    hue_bar = create_hue_gradient()

    x_min = int(h_min * 512 / 179)
    x_max = int(h_max * 512 / 179)

    if h_min <= h_max:
        cv.rectangle(hue_bar, (x_min, 0), (x_max, 50), (255,255,255), 2)
    else:
        # wrap-around → 두 구간 표시
        cv.rectangle(hue_bar, (0, 0), (x_max, 50), (255,255,255), 2)
        cv.rectangle(hue_bar, (x_min, 0), (511, 50), (255,255,255), 2)

    cv.imshow('hue_range', hue_bar)

    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()