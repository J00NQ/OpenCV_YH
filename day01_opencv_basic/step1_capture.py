import cv2 as cv

# 웹캠 연결
cap = cv.VideoCapture(0)
# 카메라가 열리지 않으면 에러 메시지 출력 후 종료
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# 반복문
while True:
    # 프레임 읽기
    ret, frame = cap.read()
    # 읽기 실패 시 break
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # 좌우 반전
    r_frame = cv.flip(frame, 1)
    # 프레임 표시
    cv.imshow('frame', r_frame)

    # 키 입력 대기 (한 번만 호출)
    k = cv.waitKey(1)
    # 'c' → my_photo.png로 저장 + "캡쳐 완료!" 출력 후 break
    if k == ord("c"):
        cv.imwrite("./captures/my_photo.png", r_frame)
        print("캡쳐 완료!")
        break
    # 'q' → break
    if k == ord("q"):
        break

# 카메라 해제 + 창 닫기
