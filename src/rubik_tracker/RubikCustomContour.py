import cv2
import logging
from .utils import get_distance, is_approx, show_line

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Logs to console
)


class RubikCustomContour:
    def __init__(self, contour, hierarchy, idx, hsv_frame):
        self.original_contour = contour
        self.hierarchy = hierarchy
        self._next, self._previous, self._first_child, self._parent = self.hierarchy
        self.s_contour = None
        self.center = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Contour instance created.")
        self.bBox = None
        self._cropped = None
        self._roi = None
        self.simplify_contour()
        self.get_center()
        self.getBbox()
        self.cropped_image(hsv_frame)
        self._og_frame = hsv_frame
        self.idx = idx
        self.contour_color = None

    def cropped_image(self, hsv_frame):
        if not self._cropped:
            x, y, w, h = self.getBbox()
            x = x + w // 4
            y = y + h // 4

            x_max = x + w // 2
            y_max = y + h // 2

            if x == x_max:
                x_max += 1

            if y == y_max:
                y_max += 1

            self.logger.info(f"Crop start {x} {y} to {x_max} {y_max}")
            self._cropped = hsv_frame[y:y_max, x:x_max]
            self._roi = [(x, y), (x_max, y_max)]
            self._area = w * h

        return self._cropped

    def order_contour_points(self):
        """
        Order contour points starting
        top left and going clockwise
        """
        center = self.get_center()

        self.logger.debug(f"self. center before being sorted -> {center}")
        self.logger.debug(f"self.s_contour before being sorted -> {self.s_contour}")

        sorted_corners = self.s_contour.copy()
        for point in self.s_contour:
            i = point[0]
            if i[0] < center [0]:
                if i[1] < center[1]:
                    sorted_corners[0] = i
            if i[0] < center [0]:
                if i[1] > center[1]:
                    sorted_corners[1] = i
            if i[0] > center [0]:
                if i[1] < center[1]:
                    sorted_corners[2] = i
            if i[0] > center [0]:
                if i[1] > center[1]:
                    sorted_corners[3] = i

        self.s_contour = sorted_corners.copy()

        self.logger.debug(f"self.s_contour sorted -> {self.s_contour}")

    def simplify_contour(self) -> None:
        peri = cv2.arcLength(self.original_contour, True)
        approx = cv2.approxPolyDP(self.original_contour, 0.1 * peri, True)
        self.s_contour = approx
        self.logger.debug(
            f"Original {self.original_contour}\t Approxed {self.s_contour}"
        )

    def get_center(self) -> tuple:
        if not self.center:
            self.logger.debug("Calculating center")
            M = cv2.moments(self.original_contour)
            self.logger.debug(f"CustomContour center M {M}")
            if M["m00"]:
                self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                self.logger.debug(f"Center found at {self.center}")
            else:
                x, y, w, h = self.getBbox()
                self.center = (x + w // 2, y + h // 2)
        else:
            self.logger.debug("Return previously calculated center")

        return self.center

    def getBbox(self):
        if not self.bBox:
            self.bBox = cv2.boundingRect(self.s_contour)
        return self.bBox

    def is_within_contour(self, c):
        # get contours bbox
        x1, y1, w1, h1 = self.getBbox()
        x2, y2, w2, h2 = c.getBbox()

        x1_max, y1_max = x1 + w1, y1 + h1
        x2_max, y2_max = x2 + w2, y2 + h2

        # Check for overlap
        return not (x1_max < x2 or x2_max < x1 or y1_max < y2 or y2_max < y1)

    def get_parent(self):
        return self._parent

    def get_child(self):
        return self._first_child

    def draw_candidate(self, image, color=(0, 0, 255), thickness = 2 ):
        rect = self.getBbox()
        self.logger.debug(f"Rect to draw {rect}")

        return cv2.rectangle(
            image, self.getBbox(), color, thickness=thickness, lineType=cv2.LINE_AA
        )
    def show_color(self, image, color):
        x,y,w,h = self.getBbox()
        origin = (x + w//2, y + h // 2)
        
        return cv2.putText(image,self.get_contour_color(), origin, cv2.FONT_HERSHEY_PLAIN, color=color, thickness=2, lineType=cv2.LINE_AA, fontScale=1)
        

    def show_contour(self):
        cv2.imshow("Contour", self._cropped)

    def is_valid(self):
        """
        A ------ B
        |        |
        |        |
        |        |
        C ------ D
        A contour is valid if
            it has 4 points
            the 4 angles are somewhere between 85 degrees and 95
            the length of every side is approximately the same lenght has the biggest side
            square areas cannot exceed 1/5 of the image
        """

        imgw,imgh,_ = self._og_frame.shape
        if self._area < 1000 or self._area >  3 * ( imgw*imgh // 9 ) :
            self.logger.info(f"Contour was too smal or too big {self._area}")
            return False

        
        self.logger.info(f"Contour had shape {self.s_contour.shape}")
        if self.s_contour.shape != (4, 1, 2):
            self.logger.info(
                f"Contour had shape {self.s_contour.shape} and is not valid"
            )
            return False

        self.order_contour_points()
        # unpack 4 points
        A, B, C, D = self.s_contour
        A = A[0]
        B = B[0]
        C = C[0]
        D = D[0]

        # Get sides
        AB = get_distance(A, B)
        AC = get_distance(A, C)
        DB = get_distance(D, B)
        DC = get_distance(D, C)

        biggest_side = max(AB, AC, DB, DC)
        if not (
            is_approx(AB, biggest_side, 0.8, 1.3)
            and is_approx(AC, biggest_side, 0.8, 1.3)
            and is_approx(DB, biggest_side, 0.8, 1.3)
            and is_approx(DC, biggest_side, 0.8, 1.3)
        ):
            self.logger.info("Sizes where too different")
            return False

        # get angles

        self.logger.info("Sizes where Correct")
        return True

    def get_contour_color(self):
        if self.contour_color:
            return self.contour_color

        x_r, y_r, width, height = self.getBbox()

        reference_pos_x, reference_pos_y = (x_r + (width // 2), y_r + (height // 2))
        hsv_px = self._og_frame[reference_pos_y, reference_pos_x]
        self.contour_color = " "
        if 0 <= hsv_px[1] < 45:
            self.contour_color = "White"

        if 0 < hsv_px[0] < 5 or 170 < hsv_px[0] <= 179:
            self.contour_color = "RED"

        if 7 < hsv_px[0] < 20:
            self.contour_color = "Orange"

        if 20 < hsv_px[0] < 55:
            self.contour_color = "Yellow"

        if 55 < hsv_px[0] < 85:
            self.contour_color = "Green"

        if 85 < hsv_px[0] < 115:
            self.contour_color = "Blue"
        return self.contour_color

    def __str__(self):
        return f"Custom Contour {self.s_contour} color: {self.contour_color} at {self.get_center()}"
