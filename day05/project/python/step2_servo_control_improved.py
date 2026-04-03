import cv2 as cv
import numpy as np
import serial
import time

# --- 시리얼 통신 설정 ---
try:
    ser = serial.Serial('COM5', 9600, timeout=1)
    print("아두이노 연결 성공 (COM5)")
    time.sleep(2)  
except serial.SerialException as e:
    print(f"❌ 아두이노 연결 실패: {e}")
    exit()

# --- ROI 및 드래그 관련 변수 ---
isDragging = False
x0, y0, x_curr, y_curr = -1, -1, -1, -1
roi_rect = None # (x1, y1, x2, y2)
blue, green, red = (255, 0, 0), (0, 255, 0), (0, 0, 255)

def onMouse(event, x, y, flags, param):
    global isDragging, x0, y0, x_curr, y_curr, roi_rect
    
    if event == cv.EVENT_LBUTTONDOWN:
        isDragging = True
        x0, y0 = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        if isDragging:
            x_curr, y_curr = x, y
    elif event == cv.EVENT_LBUTTONUP:
        if isDragging:
            isDragging = False
            x1, y1 = min(x0, x), min(y0, y)
            x2, y2 = max(x0, x), max(y0, y)
            if x2 - x1 > 5 and y2 - y1 > 5:
                roi_rect = (x1, y1, x2, y2)
                print(f"ROI 설정 완료: {roi_rect}")
            else:
                roi_rect = None
                print("ROI 초기화 (전체 화면)")

# --- 창 및 이벤트 설정 ---
cv.namedWindow("frame")
cv.setMouseCallback('frame', onMouse)

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("camera not detected")
    ser.close()
    exit()

# 감지할 색상 범위 정의 (초록색 + 파란색)
lower_green = np.array([35, 80, 80])
upper_green = np.array([85, 255, 255])

lower_blue = np.array([100, 80, 120])
upper_blue = np.array([130, 255, 255])

area_threshold = 1000
prev_status = None
last_command_time = 0
cooldown_period = 5.0

# 성능 측정용
last_detection_time = 0
prev_time = 0
fps = 0

print("프로그램 시작 ('q'를 누르면 종료, 화면을 드래그하여 영역 지정)")

while True:
    # 1. FPS 임시 계산
    curr_time = time.perf_counter()
    if prev_time > 0:
        fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    ret, frame = cap.read()
    if not ret: break

    # 2. ROI 영역 처리 및 시각화
    img_roi = frame
    if isDragging:
        cv.rectangle(frame, (x0, y0), (x_curr, y_curr), red, 2)

    if roi_rect:
        x1, y1, x2, y2 = roi_rect
        img_roi = frame[y1:y2, x1:x2]
        cv.rectangle(frame, (x1, y1), (x2, y2), blue, 2)

    # 3. 색상 연산 시작 시간 측정
    start_calc = time.perf_counter()

    hsv = cv.cvtColor(img_roi, cv.COLOR_BGR2HSV)
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    mask = cv.bitwise_or(mask_green, mask_blue)
    
    # 각 색상별 마스크 픽셀 면적 계산
    area_green = cv.countNonZero(mask_green)
    area_blue = cv.countNonZero(mask_blue)
    
    # 두 색상 중 하나라도 감지되었는지 판단
    is_detected = (area_green > area_threshold) or (area_blue > area_threshold)
    total_area = area_green + area_blue # 전체 면적 합산

    last_detection_time = (time.perf_counter() - start_calc) * 1000
    if is_detected:
        current_status = 'O'
        # 감지된 색상 명칭 구성
        detected_colors = []
        if area_green > area_threshold: detected_colors.append("GREEN")
        if area_blue > area_threshold: detected_colors.append("BLUE")
        
        status_text = f"DETECTED({ ' & '.join(detected_colors) }) Area:{total_area}"
        text_color = green
    else:
        current_status = 'C'
        status_text = f"NOT DETECTED (Total Area: {total_area})"
        text_color = red

    elapsed_time = time.perf_counter() - last_command_time
    if prev_status == 'O' and current_status == 'C' and elapsed_time < cooldown_period:
        # 아직 5초가 지나지 않았다면 'C' 명령을 유보하고 'O' 상태 유지
        current_status = 'O' 
        remaining = round(cooldown_period - elapsed_time, 1)
        status_text = f"HOLDING... {remaining}s (Area: {total_area})"
        text_color = (255, 165, 0) # 오렌지색

    # 5. 아두이노 명령 전송
    if current_status != prev_status:
        ser.write(current_status.encode())
        print(f"전송된 명령: {current_status}")
        if current_status == 'O': 
            last_command_time = time.perf_counter()
        prev_status = current_status

    # 6. 화면 출력
    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    cv.putText(frame, f"Real FPS: {fps:.1f}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, green, 2)
    cv.putText(frame, f"Latency: {last_detection_time:.2f}ms", (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.7, green, 2)
    cv.imshow("frame", frame)
    cv.imshow("mask", mask) # 병합된 마스크 확인용
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
ser.close() 
print("프로그램 종료")


'''
# step2_servo_control_improved.py
# REFACTOR 2 — 성능 분석 및 안정성 강화
- [x] 개선 1: FPS 표시로 시스템 성능 모니터링
- [x] 개선 2: 반응 시간 기록으로 성능 분석
- [x] 개선 3: 여러 색상을 동시에 감지
확인 포인트
- [x] FPS가 표시되는가?
- [x] 반응 시간이 기록되는가?
- [x] 여러 색상이 동시에 감지되는가?
'''
