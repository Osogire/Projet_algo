import math
from shape import Rectangle
from shape import Circle
from montecarlo import Montecalro


montecalro = Montecalro()
nbr_points = 100000

radius = 10
circle = Circle(radius)
print("-------------------Circle-------------------")
print("area with normal calcul :", radius**2 * math.pi)
print("with", nbr_points, "points in Montecarlo :")
for i in range(10):
    print(montecalro.calcul_area(circle, nbr_points))

height = 10
length = 10
rectangle = Rectangle(height, length)
print("-------------------Rectangle-------------------")
print("area with normal calcul :", height * length)
print("with", nbr_points, "points in Montecarlo :")
for i in range(10):
    print(montecalro.calcul_area(rectangle, nbr_points))