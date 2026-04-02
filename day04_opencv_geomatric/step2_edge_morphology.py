import cv2 as cv
import numpy as np
import sampledownload

# 이미지 로드
img = cv.imread(sampledownload.get_sample('moon_gray.jpg', repo='insightbook'))

if img is None:
    print("❌ 이미지를 불러올 수 없습니다.")
    exit()

# 그레이스케일 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# ============================================================
# 1. Canny 에지 검출
# ============================================================
thr1 = 50
thr2 = 150
edges = cv.Canny(gray, thr1, thr2)

# ============================================================
# 2. 모폴로지 연산 — 열기 (Opening)
# ============================================================
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
edges_cleaned = cv.morphologyEx(edges, cv.MORPH_OPEN, kernel)
edges_closed = cv.morphologyEx(edges_cleaned, cv.MORPH_CLOSE, kernel)

# ============================================================
# 3. 결과 비교 표시
# ============================================================
# 원본 → Canny → 열기 → 닫기 순서로 4개 이미지 배열
canny_color = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
cleaned_color = cv.cvtColor(edges_cleaned, cv.COLOR_GRAY2BGR)
closed_color = cv.cvtColor(edges_closed, cv.COLOR_GRAY2BGR)

top_row = np.hstack([img, canny_color])
bottom_row = np.hstack([cleaned_color, closed_color])
result = np.vstack([top_row, bottom_row])

cv.imshow('Edge Detection + Morphology', result)
cv.waitKey(0)
cv.destroyAllWindows()