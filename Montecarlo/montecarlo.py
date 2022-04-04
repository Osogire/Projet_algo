from hashlib import sha1
import random
from shape import Shape
from point import Point


class Montecalro:
    def __init__(self) -> None:
        self._points = []
        self._center = Point(0, 0)

    def calcul_area(self, shape : Shape, nbr_points):
        points_in_area = 0
        for i in range(nbr_points):
            self._points.append(Point(random.uniform(-shape.max_length - 10, shape.max_length + 10), random.uniform(-shape.max_height - 10, shape.max_height + 10)))
            if shape.encompass(self._points[-1]):
                points_in_area += 1
        return points_in_area / nbr_points * (2 * (shape.max_height + 10)) * (2 * (shape.max_length + 10))
