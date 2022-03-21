import copy
import re
from typing import List

import Course as Course
import Student as Student


class Instance:

    def __init__(self, nbr_students, nbr_courses, nbr_choices_by_student, nbr_courses_by_student, nbr_places):
        self._student = []
        self._courses = []
        self.create_courses(nbr_courses, nbr_places)
        self.create_students(nbr_students, nbr_choices_by_student, nbr_courses_by_student)
        self._to_assign = copy.copy(self.students)



    @property
    def students(self) -> 'list[Student.Student]': 
        """Les étudiants de l'intance
        """
        return self._student
    
    @students.setter
    def students(self, value):
        self._student = value

    @property
    def to_assign(self):
        """La liste des étudiants non assignés
        """
        return self._to_assign

    @property
    def to_assign_num(self) -> 'list[int]':
        """Les num des étudiants non assignés
        """
        nums = []
        for i in self.to_assign:
            nums.append(i.num)
        return nums

    @property
    def courses(self) -> 'list[Course.Course]':
        """Les cours de l'instance
        """
        return self._courses
    
    @courses.setter
    def courses(self, value):
        self._courses = value

    @property
    def global_satisfaction(self):
        """La satisfaction globale
        """
        s = 0
        for i in self.students:
            s+=i.satisfaction_value
        return s/len(self.students)

    def __str__(self):
        return "Instance :\n" + str(self._courses) + "\n-------------------\n" + str(self._student) + "\n Global Satisfaction : " + str(self.global_satisfaction) + "%"

    
    def create_courses(self, nbr_courses : int, nbr_places : int):
        """Crée les cours

        Args:
            nbr_courses (int): le nombre de cours à créer
            nbr_places (int): le nombre de places disponibles par cours
        """
        for i in range(nbr_courses):
            self.courses.append(Course.Course(i, nbr_places))

    def create_students(self, nbr_students : int, nbr_choices_by_student : int, nbr_courses : int):
        """Crée les étudiants

        Args:
            nbr_students (int): le nombre d'étudiants à créer
            nbr_choices_by_student (int): le nombre de choix de cours par étudiants
            nbr_courses (int): le nombre de cours que doit suivre l'étudiant
        """
        for i in range (nbr_students):
            self.students.append(Student.Student(i,self.courses, nbr_choices_by_student, nbr_courses))

    def close_course(self, course : Course.Course) -> List[Student.Student]:
        """Ferme un cours car complet

        Args:
            course (Course.Course): le cours à fermer

        Returns:
            List[Student.Student]: la liste d'étudiants à qui il faut attibuer tous les cours qu'il leur reste sous peine de bloquage
        """
        last_chance = []
        for student in course.students_choice:
            student.choices_remaining.remove(course)
            if student.nbr_remaining_choices + student.nbr_courses_chosen == student.nbr_courses:
                last_chance.append(student)
            elif student.nbr_remaining_choices + student.nbr_courses_chosen < student.nbr_courses:
                return None
        return last_chance