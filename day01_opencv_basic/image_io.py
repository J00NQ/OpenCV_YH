import cv2 as cv
import sys
import os
import urllib.request

def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, f"samples/{filename}")
    return cv.imread(f"samples/{filename}")

# img_path = "./samples/starry_night.jpg"
# img = cv.imread(img_path)
print("type to get file : ", end="")
my_file = input()
img = get_sample(f"{my_file}.jpg")
# img_gray = cv.imread(img_path, cv.IMREAD_GRAYSCALE)

if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Display window", img)
print(f"shape: {img.shape}")
print(f"dtype: {img.dtype}")
print(f"size: {img.size}")
k = cv.waitKey(0)

# cv.imshow("Display window", img_gray)
# print(f"shape: {img_gray.shape}")
# print(f"dtype: {img_gray.dtype}")
# print(f"size: {img_gray.size}")
# k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite(f"./samples/{my_file}.png", img)