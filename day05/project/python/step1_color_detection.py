'''라이브러리 import

웹캠을 열기
감지할 색상의 HSV 범위 설정
감지 면적 임계값 설정

반복:
  웹캠에서 프레임 읽기
  HSV 색공간으로 변환
  마스크 생성 (특정 색상만 추출)
  마스크 픽셀 면적 계산
  면적과 임계값 비교하여 상태 결정
  상태를 터미널과 화면에 표시
  'q' 키 입력 시 루프 종료

리소스 해제'''

import cv2 as cv
import numpy as np  

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("camera not detected")
    exit()

# TODO: 감지할 색상의 HSV 범위 설정 (초록)
lower_color = np.array([35, 80, 80])
upper_color = np.array([85, 255, 255])

# TODO: 감지 면적 임계값 설정
area_threshold = 1000

while True:
    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다. (카메라 연결 확인)")
        break

    # TODO: HSV 색공간으로 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # TODO: 마스크 생성 (특정 색상만 추출)
    mask = cv.inRange(hsv, lower_color, upper_color)
    # TODO: 마스크 픽셀 면적 계산
    area = cv.countNonZero(mask)
    # TODO: 면적과 임계값 비교하여 상태 결정 및 화면 표시
    if area > area_threshold:
        status_text = f"DETECTED (Area: {area})"
        text_color = (0, 255, 0) # 초록색
    else:
        status_text = f"NOT DETECTED (Area: {area})"
        text_color = (0, 0, 255) # 빨간색

    # 화면에 텍스트 출력 (좌상단 (10, 30) 위치)
    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

    # TODO: 상태를 터미널과 화면에 표시
    cv.imshow("frame", frame)
    cv.imshow("mask", mask)
    # TODO: 'q' 키 입력 시 루프 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()