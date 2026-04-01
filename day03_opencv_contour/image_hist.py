import cv2
import numpy as np
import matplotlib.pylab as plt

# 이미지를 그레이스케일로 읽기
img = cv2.imread('orange.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('img', img)

# 히스토그램 계산
hist = cv2.calcHist([img], [0], None, [256], [0, 256])

# 히스토그램 그리기
plt.plot(hist)
print("hist.shape:", hist.shape)  # (256, 1)
print("hist.sum():", hist.sum(), "img.shape:", img.shape)
plt.show()