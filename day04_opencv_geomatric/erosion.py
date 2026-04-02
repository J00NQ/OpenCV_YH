import cv2 as cv
import numpy as np
import sampledownload
from matplotlib import pyplot as plt

img_file = sampledownload.get_sample('4027.png')
img = cv.imread(img_file, cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
kernel = np.ones((5,5),np.uint8)
erosion = cv.erode(img,kernel,iterations = 1)

dilation = cv.dilate(img,kernel,iterations = 1)

opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)

closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT, kernel)

tophat = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)

blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT, kernel)

images = [img, erosion, dilation, opening, closing, gradient, tophat, blackhat]
titles = ['Original', 'Erosion', 'Dilation', 'Opening', 'Closing', 'Gradient', 'Tophat', 'Blackhat']

for i, (image, title) in enumerate(zip(images, titles)):
    plt.subplot(2, 4, i + 1)
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.xticks([])
    plt.yticks([])

plt.tight_layout()
plt.show()