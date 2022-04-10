import math
import time
import threading
from shape import Rectangle
from shape import Circle
from montecarlo import Montecarlo
from Viewer import View

circle = Circle(10)
montecarlo = Montecarlo(circle)
montecarlo.start()
view = View(montecarlo)

