import numpy as np
import cv2 as cv

drawing = False
mode = True  # True: rectangle, False: draw (circle brush)
ix, iy = -1, -1

img = np.zeros((512, 512, 3), np.uint8)
img_preview = img.copy()

def draw(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, img_preview

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            if mode:
                # 사각형 → preview
                img_preview = img.copy()
                cv.rectangle(img_preview, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                # 원 → 바로 그림 (선처럼)
                cv.circle(img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            # 사각형 → 최종 확정
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

# 설정
cv.namedWindow('image')
cv.setMouseCallback('image', draw)

while True:
    if drawing and mode:
        cv.imshow('image', img_preview)
    else:
        cv.imshow('image', img)

    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv.destroyAllWindows()