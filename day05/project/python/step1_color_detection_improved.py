'''
# step1_color_detection_improved.py
# REFACTOR 1 — 안정성 개선
- [x] 개선 1: 트랙바 추가로 HSV 범위를 실시간 조정
- [x] 개선 2: 모폴로지 Opening 연산으로 노이즈 제거
- [x] 개선 3: ROI 설정으로 처리 영역 제한
확인 포인트
- [x] 트랙바로 HSV 범위를 실시간 조정할 수 있는가?
- [x] 모폴로지로 노이즈가 제거되는가?
- [x] ROI 설정으로 처리 속도가 향상되는가?
'''

import cv2 as cv
import numpy as np  

def nothing(x):
    pass

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("camera not detected")
    exit()

isDragging = False
x_curr, y_curr = -1, -1
roi_rect = None # (x1, y1, x2, y2)
blue, green, red = (255, 0, 0), (0, 255, 0), (0, 0, 255)

def onMouse(event, x, y, flags, param):
    global isDragging, x0, y0, x_curr, y_curr, roi_rect
    
    if event == cv.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 다운
        isDragging = True
        x0, y0 = x, y
        
    elif event == cv.EVENT_MOUSEMOVE:  # 마우스 움직임
        if isDragging:
            x_curr, y_curr = x, y
            
    elif event == cv.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            # 좌표 정렬 (드래그 방향에 상관 없이 좌상단, 우하단 좌표 획득)
            x1, y1 = min(x0, x), min(y0, y)
            x2, y2 = max(x0, x), max(y0, y)
            
            # 너무 작은 영역은 무시
            if x2 - x1 > 5 and y2 - y1 > 5:
                roi_rect = (x1, y1, x2, y2)
                print(f"ROI 설정 완료: {roi_rect}")
            else:
                roi_rect = None
                print("ROI 초기화 (전체 화면)")
            


# 창 생성 및 이벤트 설정
cv.namedWindow("frame")
cv.setMouseCallback('frame', onMouse)

cv.namedWindow("trackbar")
# 초기값을 초록색 수준으로 설정 (H: 35~85)
cv.createTrackbar("H_min", "trackbar", 35, 180, nothing)
cv.createTrackbar("S_min", "trackbar", 80, 255, nothing)
cv.createTrackbar("V_min", "trackbar", 80, 255, nothing)
cv.createTrackbar("H_max", "trackbar", 85, 180, nothing)
cv.createTrackbar("S_max", "trackbar", 255, 255, nothing)
cv.createTrackbar("V_max", "trackbar", 255, 255, nothing)
cv.createTrackbar("area_threshold", "trackbar", 1000, 10000, nothing)
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
    
    # --- ROI 영역 처리 ---
    img_roi = frame
    if isDragging:
        # 드래그 중인 범위 빨간색으로 표시
        cv.rectangle(frame, (x0, y0), (x_curr, y_curr), red, 2)

    if roi_rect:
        x1, y1, x2, y2 = roi_rect
        img_roi = frame[y1:y2, x1:x2]
        # 설정된 ROI 사각형 파란색으로 표시
        cv.rectangle(frame, (x1, y1), (x2, y2), blue, 2)
    
    # 색상 감지 (H 범위를 초과하는 경우를 대비한 예외 처리 포함)
    hsv = cv.cvtColor(img_roi, cv.COLOR_BGR2HSV)
    if lower_color[0] > upper_color[0]:
        # H 수치가 순환하는 경우 (H_min > H_max, 주로 빨간색 범위 제어 시)
        # 1. H_min ~ 180 범위 감지
        lower_red = np.array([lower_color[0], lower_color[1], lower_color[2]])
        upper_red = np.array([180, upper_color[1], upper_color[2]])
        
        # 2. 0 ~ H_max 범위 감지
        lower_red2 = np.array([0, lower_color[1], lower_color[2]])
        upper_red2 = np.array([upper_color[0], upper_color[1], upper_color[2]])
        
        mask1 = cv.inRange(hsv, lower_red, upper_red)
        mask2 = cv.inRange(hsv, lower_red2, upper_red2)
        mask = cv.bitwise_or(mask1, mask2)
    else:
        # 일반적인 경우 (H_min <= H_max)
        mask = cv.inRange(hsv, lower_color, upper_color)

    # TODO: 모폴로지 Opening 연산으로 노이즈 제거
    raw_mask = mask.copy()  # 노이즈 제거 전 비교를 위한 디버깅 코드
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    # mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    # mask = cv.dilate(mask, kernel, iterations=2)
    # mask = cv.erode(mask, kernel, iterations=2)
    cv.imshow("raw_mask", raw_mask) # 노이즈 제거 전 비교를 위한 디버깅 코드
    area = cv.countNonZero(mask)

    area_threshold = cv.getTrackbarPos("area_threshold", "trackbar")
    if area > area_threshold:
        status_text = f"DETECTED (Area: {area})"
        text_color = green
    else:
        status_text = f"NOT DETECTED (Area: {area})"
        text_color = red

    # 결과 출력
    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    
    cv.imshow("frame", frame)
    cv.imshow("mask", mask)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()