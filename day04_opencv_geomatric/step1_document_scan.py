import cv2 as cv
import numpy as np
import sampledownload


# ============================================================
# 전역 변수
# ============================================================
win_name = "Document Scanning"
img = None
draw = None
rows, cols = 0, 0
pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)

# ============================================================
# 마우스 콜백 함수
# ============================================================
def onMouse(event, x, y, flags, param):
    """
    마우스로 4개 점을 클릭하면:
    1. 클릭 위치에 초록색 원 표시
    2. 4개 점 수집 후 자동으로 좌상/우상/우하/좌하 판단
    3. 원근 변환 적용
    """
    global pts_cnt, draw, pts, img
    
    if event == cv.EVENT_LBUTTONDOWN:
        # 1️⃣ 클릭한 위치에 원 표시
        cv.circle(draw, (x,y), 10, (0,255,0), -1)
        cv.imshow(win_name, draw)
        # 2️⃣ 좌표 저장
        pts[pts_cnt] = [x,y]
        pts_cnt+=1
        # 3️⃣ 4개 점 수집 완료 → 좌표 정렬 + 변환
        if pts_cnt == 4: 
        #     # 합 계산 (좌상단: 최소, 우하단: 최대)
            sm = pts.sum(axis=1)
        #     # 차 계산 (우상단: 최소, 좌하단: 최대)
            diff = np.diff(pts, axis = 1)

        #     # 변환 전 4개 좌표
            topLeft = pts[np.argmin(sm)]
            bottomRight = pts[np.argmax(sm)]
            topRight = pts[np.argmin(diff)]
            bottomLeft = pts[np.argmax(diff)]
            pts1 = np.float32([topLeft, topRight, bottomRight , bottomLeft])
        #
        #     # 변환 후 서류 크기 계산
            w1 = abs(bottomRight[0] - bottomLeft[0])
            w2 = abs(topRight[0] - topLeft[0])
            h1 = abs(topRight[1] - bottomRight[1])
            h2 = abs(topLeft[1] - bottomLeft[1])
            width = int(max([w1, w2]))
            height = int(max([h1, h2]))
        #
        #     # 변환 후 4개 좌표 (직사각형)
            pts2 = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])
        #     # 원근 변환 적용
            mtrx = cv.getPerspectiveTransform(pts1, pts2)
        #     # 결과 저장
            result = cv.warpPerspective(img, mtrx, (width, height))
            cv.imshow('scanned', result)
        #     # 초기화 (새로운 이미지 스캔 가능)


# ============================================================
# 메인 실행
# ============================================================


# 이미지 로드 (파일 또는 웹캠)
img_file = sampledownload.get_sample('paper.jpg', repo='insightbook')
img = cv.imread(img_file)

if img is None:
    print("❌ 이미지를 불러올 수 없습니다.")
    exit()

rows, cols = img.shape[:2]
draw = img.copy()

# 윈도우 표시 + 마우스 콜백 등록

cv.imshow(win_name, img)
cv.setMouseCallback(win_name, onMouse)    # 마우스 콜백 함수를 GUI 윈도우에 등록 ---④
cv.waitKey(0)
cv.destroyAllWindows()

# print("📝 사용법:")
# print("1. 이미지 위에 4개 점을 클릭하세요 (좌상단, 우상단, 우하단, 좌하단 순서 무관)")
# print("2. 4번째 점 클릭 후 자동으로 문서 스캔이 실행됩니다.")
# print("3. 'Scanned Document' 윈도우에서 결과를 확인하세요.")
#
# cv.waitKey(0)
# cv.destroyAllWindows()
