import abc
from math import radians
from point import Point


class Shape:
    def __init__(self) -> None:
        self._max_height = 0
        self._max_length = 0

    @property
    def max_height(self):
        return self._max_height

    @property
    def max_length(self):
        return self._max_length

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encompass (self, point : Point) -> bool:
        """return if a point is in the shape

        Args:
            point (Point): the point to check

        Returns:
            bool: true if the point is in the shape, false otherwhise
        """
        return

class Circle (Shape):
    def __init__(self, radius) -> None:
        super().__init__() 
        self._max_height = radius
        self._max_length = radius
        self._radius = radius

    def encompass(self, point: Point) -> bool:
        return point.distance(Point(0,0)) <= self._radius
    
    def __str__(self) -> str:
        return "Je suis un cercle de rayon " + str(self._radius)

class Rectangle (Shape):
    def __init__(self, height, length) -> None:
        super().__init__()
        self._height = height
        self._length = length
        self._max_height = height/2
        self._max_length = length/2

    def encompass(self, point: Point) -> bool:
        return -self.max_height <= point.y <= self.max_height and -self.max_length <= point.x <= self.max_length

    def __str__(self) -> str:
        return 'Je suis un carré de hauteur ' + str(self._height) + " et de largeur " + str(self._length)
        
    
