import cv2 as cv
import numpy as np
import serial
import time

try:
    ser = serial.Serial('COM5', 9600, timeout=1)
    print("아두이노 연결 성공 (COM5)")
    time.sleep(2)  # 아두이노 리부팅/안정화 대기
except serial.SerialException as e:
    print(f"❌ 아두이노 연결 실패: {e}")
    print("팁: 아두이노 IDE의 시리얼 모니터가 켜져 있는지 확인하고 닫아주세요.")
    exit()

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("camera not detected")
    ser.close()
    exit()

lower_color = np.array([35, 80, 80])
upper_color = np.array([85, 255, 255])

prev_status = None # None, 'O', 'C'
area_threshold = 1000

last_command_time = 0
cooldown_period = 5.0 # 5초 동안 열림 유지

print("프로그램 시작 ('q'를 누르면 종료)")

while True:
    ret, frame = cap.read()
    fps = cap.get(cv.CAP_PROP_FPS)
    if not ret:
        print("camera not detected")
        break

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_color, upper_color)

    area = cv.countNonZero(mask)

    if area > area_threshold:
        current_status = 'O' # Open
        status_text = f"DETECTED (Area: {area})"
        text_color = (0, 255, 0) # 초록색
    else:
        current_status = 'C' # Close
        status_text = f"NOT DETECTED (Area: {area})"
        text_color = (0, 0, 255) # 빨간색

    elapsed_time = time.time() - last_command_time
    if prev_status == 'O' and current_status == 'C' and elapsed_time < cooldown_period:
        current_status = 'O' 
        remaining = round(cooldown_period - elapsed_time, 1)
        status_text = f"HOLDING... {remaining}s (Area: {area})"
        text_color = (255, 165, 0) # 오렌지색 (대기 중)

    if current_status != prev_status:
        ser.write(current_status.encode()) # 'O' 또는 'C' 전송
        print(f"전송된 명령: {current_status} (면적: {area})")
        
        if current_status == 'O':
            last_command_time = time.time()
            
        prev_status = current_status

    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    cv.putText(frame, f"FPS: {fps:.2f}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv.imshow("frame", frame)
    
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
- [ ] 개선 2: 반응 시간 기록으로 성능 분석
- [ ] 개선 3: 여러 색상을 동시에 감지
확인 포인트
- [x] FPS가 표시되는가?
- [ ] 반응 시간이 기록되는가?
- [ ] 여러 색상이 동시에 감지되는가?
'''