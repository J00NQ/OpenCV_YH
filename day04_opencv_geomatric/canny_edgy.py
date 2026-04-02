import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# img = cv.imread('messi5.jpg', cv.IMREAD_GRAYSCALE)
# assert img is not None, "file could not be read, check with os.path.exists()"
# edges = cv.Canny(img,100,200)

# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

# plt.show()
img = cv.imread(('messi5.jpg'))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

blurred = cv.GaussianBlur(gray, (5,5), 1.5)

# 현재
edges_1 = cv.Canny(blurred, 100, 200, 4)
# 임계값 낮추기 -> 약한 에지도 검출 
edges_2 = cv.Canny(blurred, 90, 150, 4)
# 임계값  -> 약한 에지도 검출 
edges_3 = cv.Canny(blurred, 100, 300, 4)

cv.imshow("Original", img)
cv.imshow("Canny Edges (100, 200)_1", edges_1)
cv.imshow("Canny Edges (100, 200)_2", edges_2)
cv.imshow("Canny Edges (100, 200)_3", edges_3)

cv.waitKey(0)
cv.destroyAllWindows()