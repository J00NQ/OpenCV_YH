import cv2 as cv

# my_id_card.png 읽기
img = cv.imread("./captures/my_id_card.png")
if img is None:
    print("Could not read the image.")
    exit()
# 원본 복사본 만들기 — 드래그 중 이전 사각형을 지우기 위해
overlay = img.copy()
# 전역 변수: ix, iy (시작점), drawing (드래그 중 여부)
ix, iy = -1, -1
drawing = False
font = cv.FONT_HERSHEY_SIMPLEX
ROI = None

# 마우스 콜백 함수 정의
def draw(event, x, y, flags, param):
    # LBUTTONDOWN: 드래그 시작, 시작점(ix, iy) 저장
    global ix, iy, drawing, overlay, ROI
    # Region Of Interest (관심 영역)
    

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # MOUSEMOVE: 드래그 중이면
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
        #     원본에서 img 복원 (이전 사각형 제거)
            overlay = img.copy()

            x1, y1 = min(ix, x), min(iy, y)
            x2, y2 = max(ix, x), max(iy, y)
            text_y = max(y1 - 10, 20)

        #     현재 위치까지 초록색 사각형 그리기 (두께 2)
            cv.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.putText(overlay, "FACE", (x1, text_y), font, 2, 0, 2)

    # LBUTTONUP: 드래그 끝
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)

        text_y = max(y1 - 10, 20)
    #     최종 사각형 그리기
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #     사각형 위에 "FACE" 텍스트 넣기
        cv.putText(img, "FACE", (x1, text_y), font, 2, 0, 2)

        ROI = img[y1:y2, x1:x2]
        cv.imshow("ROI", ROI)

# 창 생성 + 마우스 콜백 등록
cv.namedWindow('image')
cv.setMouseCallback('image', draw)

# 반복문
while True:
    # 이미지 표시
    if drawing:
        cv.imshow('image', overlay)
    else:
        cv.imshow('image', img)

    # 키 입력 대기
    k = cv.waitKey(1) & 0xFF
    # 's' → my_id_card_final.png로 저장 후 break
    if k == ord('s'):
        cv.imwrite("./captures/my_id_card_final.png", img)
        if ROI is not None:
            cv.imwrite("./captures/ROI.png", ROI)
        print("저장 완료!")
    # esc or 'q' → break
    elif k == 27 or k == ord('q'):
        break
    
# 창 닫기
cv.destroyAllWindows()