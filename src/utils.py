import cv2

def apply_canny_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3,3), 1.2)
    cv2.imshow("Blurred", blurred)
    dst = cv2.Canny(blurred, 70,90 , None)
    cv2.imshow("Canny", dst)
    return dst


def dilate_contours(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    opened_image = cv2.morphologyEx(image,cv2.MORPH_CLOSE, kernel,iterations=4)
    cv2.imshow("eroded", opened_image)
    return opened_image
