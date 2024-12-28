import cv2

def apply_canny_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    blurred = cv2.bilateralFilter(gray, 9, 15,35)
    #cv2.imshow("Blurred", blurred)
    dst = cv2.Canny(blurred, 10,30 , None)
    #cv2.imshow("Canny", dst)
    return dst


def dilate_contours(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(image, kernel, iterations=8)
    #eroded = cv2.erode(dilated, kernel, iterations=1)
    eroded = cv2.bitwise_not(dilated)
    #cv2.imshow("eroded", eroded)
    return eroded
