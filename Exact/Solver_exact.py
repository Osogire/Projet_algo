from ast import Assign
import copy
from gettext import install
from itertools import permutations
from secrets import choice
import time
from tkinter.messagebox import NO
from turtle import st
from typing import List
from unittest import result


from instance.Course import Course

import instance.Instance as Instance
from instance.Student import Student


class Solver_exact:

    def __init__(self, instance : Instance.Instance):
        self._best_result = [None, None, None]
        self._instance = copy.deepcopy(instance) 
        self._double = []
        self.what_am_i_doing_wrong = []


    def attribute_courses(self, num : int):
        """Génère le meilleur emploi du temps

        Raises:
            ValueError: si impossible retourne une erreur
        """
        free_places = 0
        for i in self._instance.courses:
            places = i.places - i.nbr_student_choice
            if places > 0:
                free_places += places
        if (free_places > (len(self._instance.courses) * self._instance.courses[0].places - self._instance.nbr_courses_by_student * len(self._instance.students))):
            self._best_result[0] = self._best_result[1] = self._best_result[2] = None
            return

        if num == 0:
            self.CSP_create_solution()
        elif num == 1:
            self.create_other_solution()
        elif num == 2:
            return self.mix_methods()
        """if self._best_result == None:
            raise ValueError('Cannot assign courses correctly')"""

    
    def CSP_create_solution(self) -> Instance:
        """retrouve une première solution

        Returns:
            Instance: la solution trouvée
        """

        with open('exact\path.txt', 'w') as f:
            f.close()
        
        self.CSP_recursively_create_solution(copy.deepcopy(self._instance))

    def CSP_recursively_create_solution(self, instance : Instance.Instance) -> Instance.Instance:
        """utilise le CSP et backtracking pour trouver la solution

        Args:
            instance (Instance.Instance): instance sur laquelle il faut trouver la solution

        Returns:
            Instance: l'instance une fois complète
        """

        if self._best_result[0] != None:
            if instance.global_satisfaction <= self._best_result[0].global_satisfaction or self._best_result[0].global_satisfaction == 100:
                return None
        

            

        if len(instance.to_assign) == 0:
            self.write_txt_path(instance)
            if self._best_result[0] == None:
                self._best_result[0] = instance
            elif instance.global_satisfaction > self._best_result[0].global_satisfaction:
                self._best_result[0] = instance
            return None
        
        result = None
        instance.to_assign.sort()
        the_chosen_one = instance.to_assign[0]
        sorted_choices = self.CSP_sort_choices(the_chosen_one)
        #print("--------------", the_chosen_one.num, "---------------")
        for i in range (len(sorted_choices)):
            if not the_chosen_one.choices[i] in the_chosen_one.choices_remaining:
                continue
            #print (the_chosen_one.num, " : ", the_chosen_one.choices[i].num, ": ", the_chosen_one.choices_remaining_num, ": ", the_chosen_one.courses_num)
            result_AC3 = self.CSP_AC3(copy.deepcopy(the_chosen_one), i)
            if result_AC3 != None:
                result = self.CSP_recursively_create_solution(copy.deepcopy(result_AC3))
            if result != None:
                return result
            if sorted_choices[i] in the_chosen_one.choices_remaining:
                the_chosen_one.choices_remaining.remove(sorted_choices[i])
                sorted_choices[i].students_choice.remove(the_chosen_one)
                
        return None

    def CSP_AC3(self, the_chosen_one : Student, i) -> Instance:
        """vérifie en amont s'il y aura bloquage sur la solution ou non

        Args:
            the_chosen_one (Student): l'étudiant qui se voit attribuer un cours
            course (Course): le cours attribué à l'étudiant
            instance (Instance): l'instance dans laquelle ils sont

        Returns:
            Instance: None si bloquage, l'instance avec les modifications sinon
        """
        instance = the_chosen_one.instance
        course = the_chosen_one.choices[i]
        queue = []
        already_passed = []
        
        if the_chosen_one.nbr_remaining_choices + the_chosen_one.nbr_courses_chosen <= instance.nbr_courses_by_student:
            queue.append(the_chosen_one)
        elif self.CSP_assign_course(the_chosen_one, course, instance):
            return instance
        queue = self.CSP_close_course(queue, course, instance, already_passed)
        if queue == None:
            return None
        while len(queue) > 0:
            student = queue.pop(0)
            if student.nbr_remaining_choices + student.nbr_courses_chosen < instance.nbr_courses_by_student:
                return None
            remaining = copy.copy(student.choices_remaining)
            for i in range (instance.nbr_courses_by_student - student.nbr_courses_chosen):
                c = remaining[i]
                if not self.CSP_assign_course(student, c, instance):
                    queue = self.CSP_close_course(queue, c, instance, already_passed)
                    if queue == None:
                        return None
        return instance
            

    def CSP_close_course(self, queue : List[Student], course : Course, instance : Instance, already_passed : List[Student]) -> List[Student]:
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

    def CSP_assign_course(self, student : Student, course : Course, instance : Instance) -> bool:
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


    def CSP_sort_choices(self, student : Student) -> 'list[Course]':
        """trie les cours en fonction du nombre de demande et de leur place dans les choix de l'étudiant

        Args:
            student (Student): l'étudiant qui se voit trier ses cours

        Returns:
            list[Course]: les cours triés
        """
        sorted_choices = copy.copy(student.choices)
        for i in range (student.instance.nbr_courses_by_student):
            for j in range (student.instance.nbr_courses_by_student - i - 1):
                if sorted_choices[j].nbr_student_choice < sorted_choices[j+1].nbr_student_choice:
                    temp = sorted_choices[j]
                    sorted_choices[j] = sorted_choices[j+1]
                    sorted_choices[j+1] = temp
        return sorted_choices

    def write_txt_path(self, instance : Instance.Instance):
        with open('exact\path.txt', 'a') as f:
            f.write("------------------------\n")
            for course in instance.courses:
                f.write("course " + str(course.num) + ": " + str(course.student_num).replace(" ", ""))
            f.write("\n" + str(instance.global_satisfaction) + "%\n")
            f.close


    #-------------------------------------------------------------------------------------------------------------

    def create_other_solution(self):
        instance = copy.deepcopy(self._instance)
        for student in instance.students:
            for i in range (instance.nbr_courses_by_student):
                course : Course = student.choices[i]
                if len(course.students) >= course.places:
                    continue
                course.students.append(student)
                student.choices_remaining.remove(course)
                student.courses.append(course)
                if student.nbr_courses_chosen == instance.nbr_courses_by_student:
                    instance.to_assign.remove(student)
                    break
        instance.save_as_txt('exact\instance.txt')


        to_assign = copy.copy(instance.to_assign)
        for s in to_assign:
            for i in range(instance.nbr_courses_by_student - s.nbr_courses_chosen - 1):
                student = copy.copy(s)  
                choices = copy.copy(s.choices)
                temp = choices[0]
                choices[0] = choices[i+1]
                choices[i+1] = temp
                student.choices = choices
                instance.to_assign.append(student)

        list_to_assign = permutations(instance.to_assign, len(instance.to_assign))

        for i in list_to_assign:
            instance.to_assign = list(i)
            solution = self.calcul_solution(copy.deepcopy(instance))
            if  solution != False:
                #print(solution.global_satisfaction)
                if self._best_result[1] != None:
                    if solution.global_satisfaction > self._best_result[1].global_satisfaction:
                        self._best_result[1] = solution
                else:
                    self._best_result[1] = solution



    def calcul_solution(self, instance : Instance.Instance):

        #print(instance.to_assign_num)
        to_assign = copy.copy(instance.to_assign)
        for s in to_assign:
            if not self.assign_courses(instance,s):
                return False
        return instance

    def assign_courses(self, instance : Instance.Instance, student : Student):
        #print("----------next student : ", student.num)
        loop_list = []
        for i in range(1,instance.nbr_choices_by_student+1):
            #print("----------depth : ", i)
            if (self.recursively_assign_courses(student, None, i, copy.deepcopy(loop_list))):
                return True
        return False

    def recursively_assign_courses(self, student : Student, course : Course, depth, loop_list : list):
        """if course != None:
            print("student ", student.num, " recoit une demande de libération du cours ", course.num, " depth = ", depth)
        else:
            print("student ", student.num, "veut un cours en plus")"""
        end = []
        rec_end = []
        r_depth = depth
        depth += student.instance.nbr_courses_by_student
        """if course == None :
            depth += 1"""
        for i in range(depth):
            if i >= len(student.choices):
                return False
            c = student.choices[i]
            if c in student.choices_remaining:
                #print("student ", student.num, "essaie d'entrer dans le cours ", c.num)
                if c.places_remaining > 0 :
                    #print("il y a de la place")
                    if(student.depth != 0):
                        if(student.depth + 2 >= i):
                            #print("mais ",student.num," a une satisfaction value de ", student.satisfaction_value)
                            end.append([student, course, c])
                            continue
                    return self.swap_course(student, course, c, True)
                if (i >= student.instance.nbr_courses_by_student):
                    #print(r_depth, " ", i, " ", student.instance.nbr_courses_by_student)
                    r_depth = r_depth - i + student.instance.nbr_courses_by_student - 1
                    if r_depth <= 0:
                        return False
                for s in c.students:
                    #print("il veut demander à ", s.num, "de lui faire une place")
                    if (course != None):
                        if(s.depth != 0):
                            if(s.depth + 1 == i):
                                #print("mais ",s.num," a une déjà satisfaction value de ", s.satisfaction_value)
                                rec_end.append([student, course, s, c])
                                continue
                        loop_list.append(["s.num", student.num, "c.num", course.num])
                        if loop_list.count(["s.num", student.num, "c.num", course.num]) > 1:
                            continue
                        
                    
                    #print("student ", student.num, "demande une place dans le cours ", c.num, "au student ", s.num, " pour ", i - student.instance.nbr_courses_by_student + 1, " de depth")
                    if self.recursively_assign_courses(s, c, r_depth, copy.deepcopy(loop_list)):
                        if self.swap_course(student, course, c, False):
                            return True 
                    #print("--------------il n'a pas pu lui faire de la place------------")
        for i in end:
            return self.swap_course(i[0], i[1], i[2], True)
        for i in rec_end:
            if self.recursively_assign_courses(i[2], i[3], r_depth, copy.deepcopy(loop_list)):
                return self.swap_course(i[0], i[1], i[3], False)
        return False

    def swap_course(self, student : Student, course : Course, c : Course, double):
        #print("student ", student.num, " add course ", c.num)
        if course != None:
            #print("student ", student.num, " remove course ", course.num)
            if [student.num, course.num, c.num] in self._double:
                #print("cccccccccccccccc")
                return False
            if (double):
                self._double.append([student.num, course.num, c.num])
                
            if(not course in student.courses):
                #print("aaaaaaaaaa")
                return False
            student.courses.remove(course)
            course.students.remove(student)
            student.choices_remaining.append(course)
        if(not c in student.choices_remaining):
            #print("bbbbbbbbbb")
            return False
        student.courses.append(c)
        c.students.append(student)
        student.choices_remaining.remove(c)

        if student.nbr_courses_chosen == student.instance.nbr_courses_by_student and student in student.instance.to_assign:
            student.instance.to_assign.remove(student)
        #print("student ", student.num, "a ajouté le cours ", c.num)
        #if course != None:
            #print("et enlevé le cours ", course.num)
        return True

    def nbr_courses_to_attribute(self, instance : Instance.Instance):
        nbr = 0
        for i in instance.to_assign:
            temp = instance.nbr_courses_by_student - i.nbr_courses_chosen
            if temp > nbr:
                nbr = temp
        return nbr

    #--------------------------------------------------------------------------------------------------------------------------------------

    def mix_methods(self):
        instance = copy.deepcopy(self._instance)
        for student in instance.students:
            for i in range (instance.nbr_courses_by_student):
                course : Course = student.choices[i]
                if len(course.students) >= course.places:
                    continue
                course.students.append(student)
                student.choices_remaining.remove(course)
                student.courses.append(course)
                if student.nbr_courses_chosen == instance.nbr_courses_by_student:
                    instance.to_assign.remove(student)
                    break
        instance.save_as_txt('exact\instance.txt')
        self.p = 0
        for i in instance.students:
            self.p += instance.nbr_courses_by_student - i.nbr_courses_chosen
        #print(self.p)
        for i in range (instance.nbr_choices_by_student):
            #print(i)
            self.what_am_i_doing_wrong.clear()
            self.mix_recursive(copy.deepcopy(instance), i)
            if self._best_result[2] != None:
                return self.p
        """print("Unable to reach a solution with a depth of", instance.nbr_choices_by_student)
        print("Must not have asolution")"""


    def mix_recursive(self, instance : Instance.Instance, depth):
        if self._best_result[2] != None:
            if round(self._best_result[2].global_satisfaction, 6) == round(self.get_best_satisfaction(self.p), 6):
                return
        if len(instance.to_assign) == 0:
            if self._best_result[2] != None:
                if self._best_result[2].global_satisfaction < instance.global_satisfaction:
                    self._best_result[2] = instance
            else:
                self._best_result[2] = instance
            return
        
        student = instance.to_assign[0]
        #print("--------------")
        if instance.nbr_courses_by_student - student.nbr_courses_chosen - 1 == 0:
            instance.to_assign.remove(student)
        for course in student.choices_remaining:
            list_instances = self.mix_try_assign_course(student, course, depth)
            #print(len(list_instances))
            """min(depth - (student.choices.index(course) + 1) + instance.nbr_courses_by_student, depth))"""
            for i in list_instances:
                if i != None:
                    #print ("--", len(i.to_assign))
                    if i not in self.what_am_i_doing_wrong:
                        self.what_am_i_doing_wrong.append(i)
                        self.mix_recursive(i, depth)
    
    def mix_try_assign_course(self, student : Student, course : Course, depth):
        list_instances = []
        #print(student.num, "try assign course", course.num)
        if self._best_result[2] != None:
            if round(self._best_result[2].global_satisfaction, 6) == round(self.get_best_satisfaction(self.p), 6):
                return list_instances
        if min(depth - (student.choices.index(course) + 1) + student.instance.nbr_courses_by_student, depth - 1) >= 0:
            if course.places_remaining > 0:
                result = self.mix_assign_course(copy.deepcopy(student.instance), student.num, course.num)
                if result not in list_instances:
                    list_instances.append(result)
            else:
                for s in course.students:
                    #print(student.num)
                    result = self.mix_demand_exchange(s, course, min(depth - (student.choices.index(course) + 1) + student.instance.nbr_courses_by_student, depth), [])
                    for i in result:
                        instance = self.mix_assign_course(copy.deepcopy(i), student.num, course.num)
                        if instance != None and instance not in list_instances:
                            list_instances.append(instance)
        return list_instances

    def mix_demand_exchange(self, student : Student, course : Course, depth, double):
        #print("demand exchange", student.num, course.num, depth, double)
        if course.num in double:
            return []
        double.append(course.num)
        list_instances = []
        for c in student.choices_remaining:
        #for index in range(student.instance.nbr_courses_by_student, student.instance.nbr_choices_by_student):
            #c = student.choices[index]
            #if c in student.choices_remaining:
            if min(depth - (student.choices.index(c) + 1) + student.instance.nbr_courses_by_student, depth) >= 0:
                if c.places_remaining > 0 :
                    result = self.mix_exchange_courses(copy.deepcopy(student.instance), student.num, course.num, c.num)
                    if result not in list_instances:
                        list_instances.append(result)
                else:
                    for s in c.students:
                        #print(s.num)
                        result = self.mix_demand_exchange(s, c, min(depth - (student.choices.index(c) + 1) + student.instance.nbr_courses_by_student, depth), copy.deepcopy(double))
                        for i in result:
                            instance = self.mix_exchange_courses(copy.deepcopy(i), student.num, course.num, c.num)
                            if instance != None and instance not in list_instances:
                                list_instances.append(instance)
        return list_instances


    def mix_assign_course(self, instance : Instance.Instance, student_num, course_num):
        try:
            instance.students[student_num].choices_remaining.remove(instance.courses[course_num])
            instance.students[student_num].courses.append(instance.courses[course_num])
            instance.courses[course_num].students.append(instance.students[student_num])
        except:
            #print("except 1")
            return None
        if len(instance.students[student_num].courses) > instance.nbr_courses_by_student:
            #print("except 2")
            return None
        return instance
    
    def mix_exchange_courses(self, instance : Instance.Instance, num_student, num_course_erase, num_course_add):
        try:
            instance.students[num_student].courses.remove(instance.courses[num_course_erase])
            instance.students[num_student].choices_remaining.append(instance.courses[num_course_erase])
            instance.courses[num_course_erase].students.remove(instance.students[num_student])
        except:
            #print("except 3")
            return None
        return self.mix_assign_course(instance, num_student, num_course_add)

    def get_best_satisfaction(self, nbr_to_attribute):
        nbr_students = len(self._instance.students)
        nbr_courses = self._instance.nbr_courses_by_student
        percent =  ((nbr_courses - 1) * 100 + 80) / nbr_courses
        satisfaction = 100 * (nbr_students - nbr_to_attribute) + percent * nbr_to_attribute
        satisfaction /= nbr_students
        return (satisfaction)