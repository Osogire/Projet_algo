import copy
from tkinter.tix import Select
from tokenize import String
from typing import List
from typing_extensions import Self

import instance.Course as Course
import instance.Student as Student


class Instance:

    def __init__(self, nbr_students, nbr_courses, nbr_choices_by_student, nbr_courses_by_student, nbr_places):
        self._student = []
        self._courses = []
        self._nbr_courses_by_student = nbr_courses_by_student
        self._nbr_choices_by_student = nbr_choices_by_student
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
    def to_assign(self) -> 'list[Student.Student]':
        """La liste des étudiants non assignés
        """
        return self._to_assign
    
    @to_assign.setter
    def to_assign(self, value):
        self._to_assign = value

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
    def global_satisfaction(self) -> float:
        """La satisfaction globale
        """
        s = 0
        for i in self.students:
            s+=i.satisfaction_value
        return s/len(self.students)
    
    @property
    def nbr_choices_by_student(self):
        return self._nbr_choices_by_student

    @property
    def nbr_courses_by_student(self):
        return self._nbr_courses_by_student

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
            self.students.append(Student.Student(i, self))

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
            if student.nbr_remaining_choices + student.nbr_courses_chosen == self.nbr_courses_by_student:
                last_chance.append(student)
            elif student.nbr_remaining_choices + student.nbr_courses_chosen < self.nbr_courses_by_student:
                return None
        return last_chance

    def save_as_txt(self, path : String):
        with open(path, 'w') as f:
            f.write("Satisfaction Totale : " + str(self.global_satisfaction) + "%\n\n\n")
            for course in self.courses:
                f.write("Course " + str(course.num) + ":\n")
                f.write(str(course.students_choice_num).replace(" ", "") + "\n")
                f.write(str(course.student_num).replace(" ", "") + "\n\n")
            f.write("\n\n\n")
            for student in self.students:
                f.write("Student " + str(student.num) + ":\n")
                f.write(str(student.choices_num).replace(" ", "") + "\n")
                f.write(str(student.choices_remaining_num).replace(" ", "") + "\n")
                f.write(str(student.courses_num).replace(" ", "") + "\n")
                f.write(str(student.satisfaction_value) + "%\n\n")
            f.close

    def __eq__(self, other : Self) -> bool:
        if not type(other) is type(self):
            return False
        for i in range (len(self.courses)):
            if self.courses[i].student_num != other.courses[i].student_num:
                return False
        return True
            