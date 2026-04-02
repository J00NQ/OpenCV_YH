import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import sampledownload

img_file = sampledownload.get_sample('sudoku.png', 'opencv')
img = cv.imread(img_file)
h, w = img.shape[:2]
print(img.shape)

# 3개의 점의 대응관계 
#pts1 = np.float32([[50, 50], [200,50], [50, 200]])
#pts2 = np.float32([[10, 100], [200,50], [100, 250]])

# 4개의 점의 대응관계 
pts1 = np.float32([[0, 0], [w,0], [0, h], [w,h]])
pts2 = np.float32([[0, 0], [w,0], [50,h], [w-50,h]])

# 원근 변환 행렬 계산 
M = cv.getPerspectiveTransform(pts1, pts2)
dst = cv.warpPerspective(img, M, (w, h))

cv.imshow("Original", img)
cv.imshow("Perspective", dst)

cv.waitKey(0)
cv.destroyAllWindows()