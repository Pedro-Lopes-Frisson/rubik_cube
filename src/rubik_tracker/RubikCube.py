from .RubikPiece import RubikPiece
from .utils import draw_face
import cv2
import logging

# from rubik_solver import utils
import kociemba

# Configure the logging system
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Logs to console
)


class RubikCube:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._faces = {
            "upper": [
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("W", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
            ],
            "down": [
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("Y", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
            ],
            "front": [
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("R", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
            ],
            "back": [
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("O", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
            ],
            "left": [
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("G", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
            ],
            "right": [
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("B", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
                RubikPiece("-", (-1, -1)),
            ],
        }
        self._faces_colors = {
            "U": (255, 255, 255),
            "D": (0, 255, 255),
            "F": (0, 0, 255),
            "B": (0, 106, 255),
            "L": (0, 255, 0),
            "R": (255, 0, 0),
            "-": (100, 100, 100),
        }
        self._order = ['upper', 'right', 'front', 'down', 'left', 'back']
        self._num_pieces = 9

    def save_upper_face(self, pieces, frame):
        frame = frame.copy()
        self._faces["upper"] = pieces.copy()
        for i in self._faces["upper"]:
            self.logger.info(i.get_kociemba(), end="")
        self.logger.info("")

    def save_down_face(self, pieces, frame):
        self._faces["down"] = pieces.copy()
        for i in self._faces["down"]:
            self.logger.info(i.get_kociemba(), end="")
        self.logger.info("")

    def save_front_face(self, pieces, frame):
        self._faces["front"] = pieces.copy()
        for i in self._faces["front"]:
            self.logger.info(i.get_kociemba(), end="")
        self.logger.info("")

    def save_back_face(self, pieces, frame):
        self._faces["back"] = pieces.copy()
        for i in self._faces["back"]:
            self.logger.info(i.get_kociemba(), end="")
        self.logger.info("")

    def save_left_face(self, pieces, frame):
        self._faces["left"] = pieces.copy()
        for i in self._faces["left"]:
            self.logger.info(i.get_kociemba(), end="")
        self.logger.info("")

    def save_right_face(self, pieces, frame):
        self._faces["right"] = pieces.copy()
        for i in self._faces["right"]:
            self.logger.info(i.get_kociemba(), end="")
        self.logger.info("")

    def show_state(self, frame):
        """show cube state in the bottom left of the image"""
        h, w, _ = frame.shape
        h_piece, w_piece = 10, 10
        padding = 1
        # there is 9 pieces, and padding to the left and the last one on the right also
        h_face, w_face = (
            h_piece * 3,
            w_piece * 3,
        )

        h_state = 3 * h_face  # 3 verticle faces
        w_state = 4 * w_face  # 4 horizontal

        x_start = 0 + padding
        y_start = h - h_state

        frame = cv2.rectangle(
            frame, (x_start, y_start, w_state, h_state), (100, 100, 100), -1
        )

        face_arrangements = [(1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (3, 1)]

        face_arrangements = [
            (padding + x * w_face, y_start + y * h_face) for x, y in face_arrangements
        ]

        for face_pos, face in zip(face_arrangements, self._order):
            x_face_start, y_face_start = face_pos
            pieces = self._faces[face]
            draw_face(
                x_face_start,
                y_face_start,
                padding,
                h_face,
                w_face,
                h_piece,
                w_piece,
                pieces,
                frame,
            )


        return frame

    def solve(self, level="Beginner"):
        self._cube_string = ""
        for i in self._order:
            self._faces[i].sort()
            self._cube_string += "".join([p.get_kociemba() for p in self._faces[i][:9]])
        solve_string = None
        try:
            solve_string = kociemba.solve(self._cube_string)
        except Exception as e:
            pass
        return solve_string
