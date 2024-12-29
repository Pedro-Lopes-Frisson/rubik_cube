import cv2

def apply_canny_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3), 1.2)
    cv2.imshow("Blurred", blurred)
    dst = cv2.Canny(blurred, 00,170 , None)
    cv2.imshow("Canny", dst)
    return dst


def dilate_contours(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(image, kernel, iterations=2)
    cv2.imshow("dilated", dilated)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    eroded = cv2.bitwise_not(dilated)
    cv2.imshow("eroded", eroded)
    return eroded
