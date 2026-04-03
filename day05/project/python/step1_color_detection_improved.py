'''
# step1_color_detection_improved.py
# REFACTOR 1 — 안정성 개선
- [ ] 개선 1: 트랙바 추가로 HSV 범위를 실시간 조정
- [ ] 개선 2: 모폴로지 Opening 연산으로 노이즈 제거
- [ ] 개선 3: ROI 설정으로 처리 영역 제한
확인 포인트
- [ ] 트랙바로 HSV 범위를 실시간 조정할 수 있는가?
- [ ] 모폴로지로 노이즈가 제거되는가?
- [ ] ROI 설정으로 처리 속도가 향상되는가?
'''

import cv2 as cv
import numpy as np  

def nothing(x):
    pass

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("camera not detected")
    exit()


# TODO: 트랙바 추가로 HSV 범위를 실시간 조정
cv.namedWindow("trackbar")
cv.createTrackbar("H_min", "trackbar", 0, 180, nothing)
cv.createTrackbar("S_min", "trackbar", 0, 255, nothing)
cv.createTrackbar("V_min", "trackbar", 0, 255, nothing)
cv.createTrackbar("H_max", "trackbar", 0, 180, nothing)
cv.createTrackbar("S_max", "trackbar", 0, 255, nothing)
cv.createTrackbar("V_max", "trackbar", 0, 255, nothing)

area_threshold = 1000

while True:
    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다. (카메라 연결 확인)")
        break

    h_min = cv.getTrackbarPos("H_min", "trackbar")
    s_min = cv.getTrackbarPos("S_min", "trackbar")
    v_min = cv.getTrackbarPos("V_min", "trackbar")
    h_max = cv.getTrackbarPos("H_max", "trackbar")
    s_max = cv.getTrackbarPos("S_max", "trackbar")
    v_max = cv.getTrackbarPos("V_max", "trackbar")
    lower_color = np.array([h_min, s_min, v_min])
    upper_color = np.array([h_max, s_max, v_max])
    # TODO: ROI 설정으로 처리 영역 제한

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_color, upper_color)

    # TODO: 모폴로지 Opening 연산으로 노이즈 제거
    area = cv.countNonZero(mask)
    if area > area_threshold:
        status_text = f"DETECTED (Area: {area})"
        text_color = (0, 255, 0) # 초록색
    else:
        status_text = f"NOT DETECTED (Area: {area})"
        text_color = (0, 0, 255) # 빨간색

    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

    cv.imshow("frame", frame)
    cv.imshow("mask", mask)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()