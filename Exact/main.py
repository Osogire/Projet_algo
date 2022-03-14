import sys
sys.path.append('.')
sys.setrecursionlimit(3000)

import instance.Instance as Instance
import Solver_exact

#pour créer une instance : nbr_student(1), nbr_courses_available(2), nbr_choices(3), nbr_courses_by_student(4), nbr_places_by_courses(5)
#plus le nombre de choix diminue, plus la difficulté augmente
#plus nbr_student*nbr_courses_by_student se rapproche de nbr_courses_available*nbr_places_by_courses, plus la difficulté augmente
# == plus (1)*(4) se rapproche de (2)*(5), plus la difficulté augmente
instance = Instance.Instance(100, 20, 7, 4, 22)
#print(instance,"\n\n")
solver = Solver_exact.Solver_exact(instance)
solver.attribute_courses()
print(solver._best_result)

