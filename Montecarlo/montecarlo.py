import math
import time
from hashlib import sha1
import random
from shape import Shape
from point import Point
from Viewer import View
import threading


class Montecarlo(threading.Thread):
    def __init__(self, shape: Shape) -> None:
        threading.Thread.__init__(self)
        self._points = []
        self._center = Point(0, 0)
        self._shape = shape
        self._view = None

    def add_point(self):
        x = random.uniform(-self._shape.max_length - 10, self._shape.max_length + 10)
        y = random.uniform(-self._shape.max_height - 10, self._shape.max_height + 10)
        self._points.append(Point(x, y))
        if self._view != None:
            self._view.numberOfPointsLabel.configure(text=str(len(self._points)))
        return x, y

    def clear_points(self):
        self._points.clear()

    def calcul_area(self):
        points_in_area = 0
        for point in self._points:
            if self._shape.encompass(point):
                points_in_area += 1
        area = points_in_area / len(self._points) * (2 * (self._shape.max_height + 10)) * (
                2 * (self._shape.max_length + 10))
        if self._view != None:
            self._view.areaLabel.configure(text=str(area))
        return area

    def set_view(self, view: View):
        self._view = view

    def run(self) -> None:
        time.sleep(1)
        self.clear_points()
        if self._view != None:
            self._view.expectedAreaLabel.configure(text=str(self._shape._radius ** 2 * math.pi))
        i = 0
        while (True):
            pos = self.add_point()
            if i % 10 == 0:
                self._view.create_circle_in_can_at(pos[0], pos[1], 0.12, "red")

            if i == 2000:
                self.calcul_area()
                i = 0
            i += 1
