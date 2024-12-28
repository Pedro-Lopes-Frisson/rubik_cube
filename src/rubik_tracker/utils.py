import cv2
import numpy as np
import math


def get_distance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


def is_approx(o, o1, thresholdLow=0.9, thresholdHigh=1.1):
    print(o)
    print(o1)
    if o * thresholdLow < o1 < o * thresholdHigh:
        return True
    if o1 * thresholdLow < o < o1 * thresholdHigh:
        return True

    return False


def get_angle(p1, p2, p3):
    p12 = get_distance(p1, p2)
    p13 = get_distance(p1, p3)
    p23 = get_distance(p2, p3)
    degree_rads = math.acos((p12**2,p13**2-p23**2)/(2*p12*p13))
    return math.round(360*degree_rads/2 * np.pi)

def show_line(p1,p2, frame):
    cv2.line(frame, p1,p2,color=(10,100,200), thickness= 2, lineType=cv2.LINE_AA)
    cv2.imshow("line", frame)
    cv2.waitKey()
