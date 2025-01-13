import cv2
import numpy as np
import math


def get_distance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


def is_approx(o, o1, thresholdLow=0.9, thresholdHigh=1.1):
    if o * thresholdLow < o1 < o * thresholdHigh:
        return True
    if o1 * thresholdLow < o < o1 * thresholdHigh:
        return True

    return False


def get_angle(p1, p2, p3):
    p12 = get_distance(p1, p2)
    p13 = get_distance(p1, p3)
    p23 = get_distance(p2, p3)
    degree_rads = math.acos((p12**2, p13**2 - p23**2) / (2 * p12 * p13))
    return math.round(360 * degree_rads / 2 * np.pi)


def show_line(p1, p2, frame):
    cv2.line(frame, p1, p2, color=(10, 100, 200), thickness=2, lineType=cv2.LINE_AA)
    cv2.imshow("line", frame)
    cv2.waitKey()


def get_color(roi):
    roi_cp = roi.copy()

    r, c, channels = roi_cp.shape

    # roi_cp = roi_cp.reshape((r*c, channels))
    mean_color = roi_cp[7 * r // 8, c // 8]

    h, s, v = mean_color

    # Classify based on HSV thresholds
    if s < 50 and v > 200:
        return "White"
    elif 0 <= h <= 10 or 170 <= h <= 179:
        return "Red"
    elif 11 <= h <= 18:
        return "Orange"
    elif 19 <= h <= 35:
        return "Yellow"
    elif 36 <= h <= 85:
        return "Green"
    elif 86 <= h <= 125:
        return "Blue"
    else:
        return "Unknown"


def draw_face(
    x_start, y_start, padding, h_face, y_face, h_piece, w_piece, pieces, frame
):
    _faces_colors = {
        "U": (255,255,255),
        "D": (0, 200, 255),
        "F": (0, 0, 255),
        "B": (0, 106, 255),
        "L": (0, 255, 0),
        "R": (255, 0, 0),
        "-": (100, 100, 100),
    }
    # draw left face
    face_start_x = x_start
    face_start_y = y_start
    square_arrangements = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ]

    for (row_number, col_number), piece in zip(square_arrangements, pieces):
        face_start_x = x_start + w_piece * col_number
        face_start_y = y_start + h_piece * row_number

        frame = cv2.rectangle(
            frame,
            (face_start_x, face_start_y, w_piece, h_piece),
            # self._faces_colors[i.get_kociemba()],
            _faces_colors[piece.get_kociemba()],
            -1,
        )


if __name__ == "__main__":
    import random

    roi = np.zeros((2, 2, 3))
    for x in range(2):
        for y in range(2):
            for c in range(3):
                roi[x, y][c] = random.randint(0, 10)

    get_color(roi)
