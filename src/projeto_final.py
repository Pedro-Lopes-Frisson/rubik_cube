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

    cv2.namedWindow("Blurred", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("video", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("Canny", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("dilated", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("eroded", cv2.WINDOW_FREERATIO)

    capture = cv2.VideoCapture("src\\20241128_111931.mp4")
    #capture = cv2.VideoCapture("./20241128_111931.mp4")
    #capture = cv2.VideoCapture("./20241123_182441.mp4")
    #capture = cv2.VideoCapture("src\\20241123_182441.mp4")


    capture = cv2.VideoCapture(0)
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
        contours, hierarchy = cv2.findContours(dilated_canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        if hierarchy is None:
            hierarchy=[[]]
        custom_contours = []
        indices =  range(len(contours) +1 )
        for idx, contour, h in zip(indices,contours,hierarchy[0]):
            c_c = RubikCustomContour(contour, h, idx, hsv_frame)
            custom_contours.append(c_c)
        
        for c_c in custom_contours:
            if c_c.is_valid():
                frame = c_c.draw_candidate(frame, color=(255,0,0), thickness=3 )
            else:
                frame =  c_c.draw_candidate(frame, color=(0,0,255), thickness=4 )
        
        remove_duplicates = set()
        for c_c in custom_contours:
            if not c_c.is_valid() or any([c_c.is_within_contour(c)  for c in remove_duplicates]):
                continue
            last_cc_valid  = c_c
            if c_c.get_child() != -1:
                _,_,child, parent = hierarchy[0][c_c.idx]
                while child != -1:
                    child_cc = custom_contours[child]
                    if child_cc.is_valid():
                        last_cc_valid = child_cc
                    if child == -1:
                        break
                    h_child = hierarchy[0][child]
                    _,_,child, parent = h_child
            
            last_cc_valid.draw_candidate(frame, color=(0,255,0), thickness = 2)
            last_cc_valid.show_color(frame, color=(255,100,100))
            remove_duplicates.add(last_cc_valid)
        
#       for c in non_overlapping_contours:
#           c_c_valid =  RubikCustomContour(contours[c], hierarchy[0][c], c, hsv_frame)
#           frame = c_c_valid.draw_candidate(frame, color=(255,0,0))
#           print(c, hierarchy[0][c])

        



        #print(non_overlapping_contours)
        cv2.imshow("video", frame)
        ret, frame = capture.read()
        hand_keyboard()
