from .utils import get_distance


class RubikPiece:
    def __init__(self, color, center):
        self.color = color
        self.center = center
        self._kociemba_notation = {
            "W": "U",
            "R": "F",
            "G": "L",
            "Y": "D",
            "O": "B",
            "B": "R",
            "-": "-", # uninitialized state
            "U": "-", # Bad color
        }

    def get_kociemba(self):
        return self._kociemba_notation[self.color[0]]

    def __eq__(self, o):
        if self.color != self.color:
            return False
        if get_distance(o.center, self.center) < 10:
            return True

    def __gt__(self, o):
        center_x1, center_y1 = self.center
        center_x2, center_y2 = o.center
        y_threshold = 10

        return (center_y1 > center_y2 + 10, center_x1 > center_x2)

    def __lt__(self, o):
        center_x1, center_y1 = self.center
        center_x2, center_y2 = o.center
        y_threshold = 10

        return (center_y2 > center_y1 + 10, center_x2 > center_x1)

    def __str__(self):
        return f"{self.center=:} with color {self.color}"

    def __repr__(self):
        return f"{self.center=:} with color {self.color}"


if __name__ == "__main__":
    a = RubikPiece("blue", (10, 4))
    b = RubikPiece("blue", (10, 10))
    c = RubikPiece("blue", (20, 4))
    d = RubikPiece("blue", (20, 8))

    print("a > b: ", a > b)
    print("a < b: ", a < b)

    print("c > d: ", c > d)
    print("c < d: ", c < d)

    print("b > d: ", b > d)
    print("b < d: ", b < d)

    lst = [d, c, b, a]
    lst = sorted(lst)
    print(lst)
