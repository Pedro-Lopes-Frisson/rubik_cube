import cv2
from rubik_tracker.RubikCustomContour import RubikCustomContour
from rubik_tracker.RubikCube import RubikCube
from rubik_tracker.RubikPiece import RubikPiece
from utils import apply_canny_detection, dilate_contours
import sys
import time
import numpy as np

if __name__ == "__main__":

    cv2.namedWindow("Blurred", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("video", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("Canny", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("dilated", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("eroded", cv2.WINDOW_FREERATIO)
    cv2.namedWindow("hsv", cv2.WINDOW_FREERATIO)

    cube = RubikCube()
    try:
        # capture = cv2.VideoCapture("src\\20241128_111931.mp4")
        # capture = cv2.VideoCapture("./src/20241128_111931.mp4")
        # capture = cv2.VideoCapture("./20241123_182441.mp4")
        # capture = cv2.VideoCapture("src\\20241123_182441.mp4")
        # capture = cv2.VideoCapture(0)
        # capture = cv2.VideoCapture("http://192.168.1.68:4747/video")
        capture = cv2.VideoCapture("http://192.168.1.86:4747/video")
        # capture = cv2.VideoCapture("http://192.168.241.75:4747/video")

        # capture.set(cv2.CAP_PROP_FPS, 15)
        capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        capture.set(cv2.CAP_PROP_FOCUS, 10)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # 1080, 720, 360
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 1920, 1280, 640

    except Exception as e:
        print(e)
        sys.exit(1)

    timeout = 0
    ret, frame = capture.read()
    height, width = frame.shape[:2]
    frame_count = 1
    image_center = (height // 2, width // 2)
    gamma = 1.9

    invGamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")

    saved_candidates = []
    solve_string = ""

    while capture.isOpened():
        """
        http://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
        """
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values

        # apply gamma correction using the lookup table

        original_frame = frame.copy()
        frame = cv2.LUT(frame, table)

        # cv2.imshow("og_gramne", original_frame)

        cv2.imshow("video", frame)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("hsv", hsv_frame)

        canny = apply_canny_detection(frame)
        dilated_canny = dilate_contours(canny)

        contours, hierarchy = cv2.findContours(
            dilated_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )

        if hierarchy is None:
            hierarchy = [[]]
        custom_contours = []
        indices = range(len(contours) + 1)
        for idx, contour, h in zip(indices, contours, hierarchy[0]):
            c_c = RubikCustomContour(contour, h, idx, hsv_frame)
            custom_contours.append(c_c)

        """
        for c_c in custom_contours:
            if c_c.is_valid():
                frame = c_c.draw_candidate(frame, color=(255,0,0), thickness=3 )
            else:
                frame =  c_c.draw_candidate(frame, color=(0,0,255), thickness=4 )
        """

        valid_candidates = []
        for c_c in custom_contours:
            if not c_c.is_valid() or any(
                [c_c.is_within_contour(c) for c in valid_candidates]
            ):
                continue
            last_cc_valid = c_c
            if c_c.get_child() != -1:
                _, _, child, parent = hierarchy[0][c_c.idx]
                while child != -1:
                    child_cc = custom_contours[child]
                    if child_cc.is_valid():
                        last_cc_valid = child_cc
                    if child == -1:
                        break
                    h_child = hierarchy[0][child]
                    _, _, child, parent = h_child
            if not (last_cc_valid.get_area() > height * width // 6):
                valid_candidates.append(last_cc_valid)

        if valid_candidates != []:
            avg = sum([c.get_area() for c in valid_candidates]) / len(valid_candidates)

            valid_candidates_copy = valid_candidates.copy()
            valid_candidates = []
            for i in range(len(valid_candidates_copy)):
                if not (
                    valid_candidates_copy[i].get_area() < (avg * 5) / 8
                    or valid_candidates_copy[i].get_area() > 14 / 10 * avg
                ):
                    valid_candidates.append(valid_candidates_copy[i])
            valid_candidates_copy = []

        if len(valid_candidates) == 9:
            saved_candidates = valid_candidates.copy()

        for v_c in saved_candidates:
            v_c.draw_candidate(frame, color=(0, 255, 255), thickness=2)
            v_c.show_color(frame, color=(255, 100, 100))

        frame = cube.show_state(frame)

        if solve_string is None:
            frame = cv2.putText(frame, "Invalid Cube string", (10,40), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), thickness=2, lineType=cv2.LINE_AA)
            cv2.imshow("video", frame)
        cv2.imshow("video", frame)
        ret, frame = capture.read()

        k = ""
        try:
            k = chr(cv2.waitKey(1))
        except:
            pass
        if k == "f":
            print("Save Front Face: ")
            print(len(saved_candidates))
            cube_face = []
            for i in saved_candidates:
                cube_face.append(RubikPiece(i.get_contour_color(), i.get_center()))
            cube.save_front_face(sorted(cube_face), hsv_frame)
        if k == "b":
            print("Save back face")
            cube_face = []
            for i in saved_candidates:
                cube_face.append(RubikPiece(i.get_contour_color(), i.get_center()))
            cube.save_back_face(sorted(cube_face), hsv_frame)
        if k == "u":
            print("Save upper face")
            print(len(saved_candidates))
            cube_face = []
            for i in saved_candidates:
                cube_face.append(RubikPiece(i.get_contour_color(), i.get_center()))
            cube.save_upper_face(sorted(cube_face), hsv_frame)
        if k == "d":
            print("Save down face")
            cube_face = []
            for i in saved_candidates:
                cube_face.append(RubikPiece(i.get_contour_color(), i.get_center()))
            cube.save_down_face(sorted(cube_face), hsv_frame)
        if k == "l":
            print("Save left face")
            cube_face = []
            for i in saved_candidates:
                cube_face.append(RubikPiece(i.get_contour_color(), i.get_center()))
            cube.save_left_face(sorted(cube_face), hsv_frame)
        if k == "r":
            print("Save right face")
            cube_face = []
            for i in saved_candidates:
                cube_face.append(RubikPiece(i.get_contour_color(), i.get_center()))
            cube.save_right_face(sorted(cube_face), hsv_frame)

        if k == "s":
            solve_string = cube.solve()
            print(solve_string)

        if k == "q":
            cv2.destroyAllWindows()
            sys.exit(0)
