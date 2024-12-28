import cv2
from rubik_tracker.RubikCustomContour import RubikCustomContour
from utils import apply_canny_detection, dilate_contours
import sys
import time

def hand_keyboard():
    k = ""
    try:
        k = chr(cv2.waitKey(1))
    except:
        pass
    if k == "q":
        cv2.destroyAllWindows()
        sys.exit(0)

    if k == "h":
        cv2.waitKey()


if __name__ == "__main__":

    cv2.namedWindow("video", cv2.WINDOW_FREERATIO)
    #capture = cv2.VideoCapture("src\\20241123_182441.mp4")
    #capture = cv2.VideoCapture("./20241128_111931.mp4")
    #capture = cv2.VideoCapture("./20241123_182441.mp4")
    capture = cv2.VideoCapture("src\\20241123_182441.mp4")


    #capture = cv2.VideoCapture(0)
    # capture = cv2.VideoCapture("http://192.168.241.75:4747/video")
    #capture = cv2.VideoCapture("http://192.168.1.68:4747/video")

    while capture.isOpened() == False:
        time.sleep(1)

    ret, frame = capture.read()
    height, width = frame.shape[:2]
    frame_count = 1
    image_center = (height // 2, width // 2 )
    while capture.isOpened():

        original_frame = frame.copy()


        #cv2.imshow("og_gramne", original_frame)

        cv2.imshow("video", frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        canny = apply_canny_detection(frame)
        dilated_canny = dilate_contours(canny)
        contours, hierarchy = cv2.findContours(dilated_canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        custom_contours = []
        indices =  range(len(contours) +1 )
        for idx, contour, h in zip(indices,contours,hierarchy[0]):
            if not( contour.shape[0]> 4):
                continue
            c_c = RubikCustomContour(contour, h, idx, hsv_frame)
            if c_c.is_valid():
                _,_,child, parent = h
                last_cc_valid  = None
                while child != -1:
                    child_cc = RubikCustomContour(contour, h, idx, hsv_frame)
                    if child_cc.is_valid():
                        last_cc_valid = child_cc
                    else:
                        break
                    _,_,child, parent = h
                if last_cc_valid:
                    custom_contours.append(last_cc_valid)
                else:
                    custom_contours.append(c_c)
        
        for c_c in custom_contours:
            frame = c_c.draw_candidate(frame)

#       non_overlapping_contours = set()
#       for c_c in custom_contours:
#           for c_c1 in custom_contours:
#               if c_c.is_within_contour(c_c1) and (c_c.get_child() == -1 or c_c1.get_child() == c_c.idx ) :
#                   non_overlapping_contours.add(c_c.idx)

#       for c in non_overlapping_contours:
#           c_c_valid =  RubikCustomContour(contours[c], hierarchy[0][c], c, hsv_frame)
#           frame = c_c_valid.draw_candidate(frame, color=(255,0,0))
#           print(c, hierarchy[0][c])

        #print(non_overlapping_contours)
        cv2.imshow("video", frame)
        ret, frame = capture.read()
        hand_keyboard()
