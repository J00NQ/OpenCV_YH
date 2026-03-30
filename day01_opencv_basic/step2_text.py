import cv2 as cv

# my_photo.png 읽기
img = cv.imread(f"./captures/my_photo.png")
# 이미지 높이(h), 너비(w) 가져오기 — img.shape[:2]

print(f"shape: {img.shape}")
# --- 하단 반투명 배경 바 ---
# 1) overlay = img.copy()
overlay = img.copy()
# 2) overlay 하단 80px 영역에 검정 사각형 채우기 (thickness=-1)
cv.rectangle(overlay, (0, 400), (640, 480), 0, -1)
# 3) addWeighted로 img와 overlay를 50:50 합성
img = cv.addWeighted(img, 0.5, overlay, 0.5, 1)

# --- 텍스트 ---
# 이름 텍스트 넣기 (putText) — 하단 배경 바 안쪽 위치
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'MY_NAME',(100,440), font, 1,(255,255,255),2,cv.LINE_AA)
# 소속 텍스트 넣기 (putText) — 이름 아래에 작은 크기로
cv.putText(img,'YH',(100,470), font, 0.8,(255,255,255),1,cv.LINE_AA)
# 결과 표시 + 키 입력 대기
cv.imshow("Display window", img)
k = cv.waitKey(0)
# my_id_card.png로 저장
if k == ord("s"):
    cv.imwrite("./captures/my_id_card.png", img)
    print("저장 완료!")
# 창 닫기
