import cv2
import numpy as np


def apply_canny_detection(image, sigma=0.30):

    blurred = cv2.GaussianBlur(image, (3, 3), 0.5)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    v = np.median(gray)
    _, gray = cv2.threshold(gray, 90, 0, cv2.THRESH_TOZERO)

    cv2.imshow("Gray", gray)
    # apply automatic Canny edge detection using the computed median
    # https://pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    dst = cv2.Canny(gray, lower, upper)

    cv2.imshow("Canny", dst)
    return dst


def dilate_contours(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
    opened_image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations=5)
    opened_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, kernel, iterations=1)

    opened_image = cv2.bitwise_not(opened_image)
    cv2.imshow("eroded", opened_image)
    return opened_image


def simplify_solve_string(solve_string):
    moves_simple = {
        "U2": ["U", "U"],
        "L2": ["L", "L"],
        "R2": ["R", "R"],
        "D2": ["D", "D"],
        "F2": ["F", "F"],
        "B2": ["T", "T", "F", "F", "T'", "T'"],
        "B": ["T", "T", "F", "T'", "T'"],
        "B'": ["T", "T", "F'", "T'", "T'"],
    }
    simple_string = ""
    complex_moves = moves_simple.keys()
    solve_string_moves = solve_string.split(" ")
    for move in solve_string_moves:
        if move in complex_moves:
            simple_string += " ".join(moves_simple[move]) + " "
        else:
            simple_string += move + " "
    print(simple_string)
    return simple_string


def draw_instruction(movement, frame):
    """Get the movement and draw the steps to solve it"""
    if movement == "":
        return frame
    h, w = frame.shape[:2]

    mid_x, mid_y = w // 2, h // 2
    start_x, end_x = mid_x - 40, mid_x + 40
    start_y, end_y = mid_y - 40, mid_y + 40

    move_line_mapping = {
        "U": {
            "lines": [cv2.arrowedLine, cv2.line, cv2.line],
            "points": [
                [(end_x, mid_y - 40), (start_x, mid_y - 40)],
                [(start_x, mid_y), (end_x, mid_y)],
                [(start_x, mid_y + 40), (end_x, mid_y + 40)],
            ],
        },
        "U'": {
            "lines": [cv2.arrowedLine, cv2.line, cv2.line],
            "points": [
                [(start_x, mid_y - 40), (end_x, mid_y - 40)],
                [(start_x, mid_y), (end_x, mid_y)],
                [(start_x, mid_y + 40), (end_x, mid_y + 40)],
            ],
        },
        "D": {
            "lines": [cv2.line, cv2.line, cv2.arrowedLine],
            "points": [
                [(start_x, mid_y - 40), (end_x, mid_y - 40)],
                [(start_x, mid_y), (end_x, mid_y)],
                [(start_x, mid_y + 40), (end_x, mid_y + 40)],
            ],
        },
        "D'": {
            "lines": [cv2.line, cv2.line, cv2.arrowedLine],
            "points": [
                [(start_x, mid_y - 40), (end_x, mid_y - 40)],
                [(start_x, mid_y), (end_x, mid_y)],
                [(end_x, mid_y + 40), (start_x, mid_y + 40)],
            ],
        },
        "T": {
            "lines": [cv2.arrowedLine, cv2.arrowedLine, cv2.arrowedLine],
            "points": [
                [(end_x, mid_y - 40), (start_x, mid_y - 40)],
                [(end_x, mid_y), (start_x, mid_y)],
                [(end_x, mid_y + 40), (start_x, mid_y + 40)],
            ],
        },
        "T'": {
            "lines": [cv2.arrowedLine, cv2.arrowedLine, cv2.arrowedLine],
            "points": [
                [(start_x, mid_y - 40), (end_x, mid_y - 40)],
                [(start_x, mid_y), (end_x, mid_y)],
                [(start_x, mid_y + 40), (end_x, mid_y + 40)],
            ],
        },
        "L": {
            "lines": [cv2.arrowedLine, cv2.line, cv2.line],
            "points": [
                [(mid_x - 40, start_y), (mid_x - 40, end_y)],
                [(mid_x, start_y), (mid_x, end_y)],
                [(mid_x + 40, start_y), (mid_x + 40, end_y)],
            ],
        },
        "L'": {
            "lines": [cv2.arrowedLine, cv2.line, cv2.line],
            "points": [
                [(mid_x - 40, end_y), (mid_x - 40, start_y)],
                [(mid_x, start_y), (mid_x, end_y)],
                [(mid_x + 40, start_y), (mid_x + 40, end_y)],
            ],
        },
        "R": {
            "lines": [cv2.line, cv2.line, cv2.arrowedLine],
            "points": [
                [(mid_x - 40, end_y), (mid_x - 40, start_y)],
                [(mid_x, start_y), (mid_x, end_y)],
                [(mid_x + 40, start_y), (mid_x + 40, end_y)],
            ],
        },
        "R'": {
            "lines": [cv2.line, cv2.line, cv2.arrowedLine],
            "points": [
                [(mid_x - 40, start_y), (mid_x - 40, end_y)],
                [(mid_x, start_y), (mid_x, end_y)],
                [(mid_x + 40, start_y), (mid_x + 40, end_y)],
            ],
        },
    }
    if "F" not in movement:
        things = move_line_mapping[movement]
        for line, points in zip(things["lines"], things["points"]):
            line(
                frame,
                points[0],
                points[1],
                (200, 100, 50),
                thickness=3,
            )
    if "F" in movement:
        frame = cv2.circle(frame, (mid_x,mid_y), 40, (200,100,50), thickness=3)
        if "'" in movement:
            frame = cv2.arrowedLine(frame, (mid_x-40,mid_y-1), (mid_x-40,mid_y+1), (200,100,50), tipLength=6, thickness=2)
        else:
            frame = cv2.arrowedLine(frame, (mid_x-40,mid_y+1),(mid_x-40,mid_y-1) , (200,100,50), tipLength=6, thickness=2)



    return frame


if __name__ == "__main__":
    solve_string = "U R2 U' B2 D' L B D2 B2 L D2 B2 L2 B2 D' L2 D' B2 L2 B2"
    simple = simplify_solve_string(solve_string).split(" ")
    frame = np.ones((720, 480, 3), dtype=np.uint8) * 255
    cv2.imshow("video", frame)
    for move in simple:
        new_frame = draw_instruction(move, frame.copy())
        new_frame = cv2.putText(
            new_frame, move, (40, 40), cv2.FONT_HERSHEY_PLAIN, 1, (200, 100, 50)
        )
        cv2.imshow("video", new_frame)
        cv2.waitKey()
    cv2.destroyAllWindows()
