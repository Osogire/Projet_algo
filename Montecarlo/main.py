import math
from shape import Rectangle
from shape import Circle
from montecarlo import Montecarlo



nbr_points = 100000

radius = 10
circle = Circle(radius)
montecarlo = Montecarlo(circle)
print("-------------------Circle-------------------")
print("area with normal calcul :", radius**2 * math.pi)
print("with", nbr_points, "points in Montecarlo :")
for i in range(10):
    montecarlo.clear_points()
    for i in range(nbr_points) :
        montecarlo.add_point()
    print(montecarlo.calcul_area())


height = 10
length = 10
rectangle = Rectangle(height, length)
montecarlo = Montecarlo(rectangle)
print("-------------------Rectangle-------------------")
print("area with normal calcul :", height * length)
print("with", nbr_points, "points in Montecarlo :")
for i in range(10):
    montecarlo.clear_points()
    for i in range(nbr_points):
        montecarlo.add_point()
    print(montecarlo.calcul_area())
