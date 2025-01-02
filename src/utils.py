import cv2
import numpy as np


def apply_canny_detection(image, sigma=0.30):

    blurred = cv2.GaussianBlur(image, (3, 3), 0.5)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    _,gray = cv2.threshold(gray, 90, 0, cv2.THRESH_TOZERO)

    cv2.imshow("Gray", gray)
    # apply automatic Canny edge detection using the computed median
    # https://pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    dst = cv2.Canny(gray, lower, upper)

    cv2.imshow("Canny", dst)
    return dst


def dilate_contours(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
    opened_image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations=5)
    opened_image = cv2.morphologyEx(
        opened_image, cv2.MORPH_CLOSE, kernel, iterations=1
    )

    opened_image = cv2.bitwise_not(opened_image)
    cv2.imshow("eroded", opened_image)
    return opened_image
