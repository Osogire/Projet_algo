import copy
from queue import PriorityQueue
from typing import List
from instance.Course import Course

import instance.Instance as Instance
from instance.Student import Student


class Solver_exact:
    _priority_queue = PriorityQueue()
    _best_result = Instance.Instance

    def __init__(self, instance : Instance.Instance):
        self._instance = copy.deepcopy(instance)


    def attribute_courses(self):
        """Génère le meilleur emploi du temps

        Raises:
            ValueError: si impossible retourne une erreur
        """
        self._best_result = self.create_first_solution()
        if self._best_result == None:
            raise ValueError('Cannot assign courses correctly')

    
    def create_first_solution(self) -> Instance:
        """retrouve une première solution

        Returns:
            Instance: la solution trouvée
        """
        return self.recursively_create_first_solution(copy.deepcopy(self._instance))

    def recursively_create_first_solution(self, instance : Instance.Instance) -> Instance:
        """utilise le CSP et backtracking pour trouver la solution

        Args:
            instance (Instance.Instance): instance sur laquelle il faut trouver la solution

        Returns:
            Instance: l'instance une fois complète
        """
        if len(instance.to_assign) == 0:
            return instance
        
        result = None
        instance.to_assign.sort()
        the_chosen_one = instance.to_assign[0]
        sorted_choices = self.sort_choices(the_chosen_one)

        for i in range (len(sorted_choices)):
            if not the_chosen_one.choices[i] in the_chosen_one.choices_remaining:
                continue
            #print(instance.to_assign_num)
            #print(the_chosen_one.num," : ", the_chosen_one.courses_num)
            course = the_chosen_one.choices[i]
            result_AC3 = self.AC3(the_chosen_one, course, instance)
            if result_AC3 != None:
                result = self.recursively_create_first_solution(copy.deepcopy(result_AC3))
            if result != None:
                return result
        return None

    def AC3(self, the_chosen_one : Student, course : Course, instance : Instance) -> Instance:
        """vérifie en amont s'il y aura bloquage sur la solution ou non

        Args:
            the_chosen_one (Student): l'étudiant qui se voit attribuer un cours
            course (Course): le cours attribué à l'étudiant
            instance (Instance): l'instance dans laquelle ils sont

        Returns:
            Instance: None si bloquage, l'instance avec les modifications sinon
        """
        queue = []
        already_passed = []
        
        if the_chosen_one.nbr_remaining_choices + the_chosen_one.nbr_courses_chosen <= the_chosen_one.nbr_courses:
            queue.append(the_chosen_one)
        elif self.assign_course(the_chosen_one, course, instance):
            return instance
        queue = self.close_course(queue, course, instance, already_passed)
        if queue == None:
            return None
        while len(queue) > 0:
            student = queue.pop(0)
            if student.nbr_remaining_choices + student.nbr_courses_chosen < student.nbr_courses:
                return None
            remaining = copy.copy(student.choices_remaining)
            for i in range (student.nbr_courses - student.nbr_courses_chosen):
                c = remaining[i]
                if not self.assign_course(student, c, instance):
                    queue = self.close_course(queue, c, instance, already_passed)
                    if queue == None:
                        return None
        return instance
            

    def close_course(self, queue : List[Student], course : Course, instance : Instance, already_passed : List[Student]) -> List[Student]:
        """ferme un cours complet

        Args:
            queue (List[Student]): la liste d'étudiant devant obligatoirement se voir attribué les cours qu'il leur reste sous peine de bloquage
            course (Course): le cours à fermer
            instance (Instance): l'instance de travail
            already_passed (List[Student]): la liste des étudiant ayant déjà été dans queue

        Returns:
            List[Student]: la queue complétée
        """
        last_chance = instance.close_course(course)
        if last_chance == None :
            return None
        for i in last_chance:
            if not i in already_passed:
                already_passed.append(i)
                queue.append(i)
        return queue

    def assign_course(self, student : Student, course : Course, instance : Instance) -> bool:
        """assigne un cours à un élève

        Args:
            student (Student): l'élève qui se voit assigner le cours
            course (Course): le cours assigné à l'élève
            instance (Instance): l'instance de travail

        Returns:
            bool: False si le cours doit fermer, True sinon
        """
        result = student.assign_course(course)
        if result[0]:
            instance.to_assign.remove(student)
        return not result[1]


    def sort_choices(self, student : Student) -> 'list[Course]':
        """trie les cours en fonction du nombre de demande et de leur place dans les choix de l'étudiant

        Args:
            student (Student): l'étudiant qui se voit trier ses cours

        Returns:
            list[Course]: les cours triés
        """
        sorted_choices = copy.copy(student.choices)
        choices = copy.copy
        for i in range (student.nbr_courses):
            for j in range (student.nbr_courses - i - 1):
                if sorted_choices[j].nbr_student_choice < sorted_choices[j+1].nbr_student_choice:
                    temp = sorted_choices[j]
                    sorted_choices[j] = sorted_choices[j+1]
                    sorted_choices[j+1] = temp
        
        return sorted_choices
        