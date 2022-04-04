from math import sqrt
from typing_extensions import Self


class Point:
    def __init__(self, x : float, y : float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def distance(self, other : Self):
        return sqrt((other.x - self._x)**2 + (other.y - self._y)**2)

    def __str__(self) -> str:
        return "(" + str(self._x) + "," + str(self._y) + ")"