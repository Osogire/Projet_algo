import copy
from pickle import TRUE
import random
from re import I
from typing import List, Tuple
from unittest import result

from sqlalchemy import false, true

import instance.Course as Course
from typing_extensions import Self




class Student:

    def __init__(self, num, courses, nbr_choice_courses, nbr_courses):
        self._num = num
        self._choices = []
        self._courses = []
        #self._satisfaction_value = 200
        self._nbr_courses = nbr_courses
        self._nbr_choices = nbr_choice_courses
        self.choose_courses(copy.copy(courses), nbr_choice_courses)
        self._choices_ramaining = copy.copy(self.choices)
        self._satisfaction_list = self.create_satisfaction_list(nbr_choice_courses, nbr_courses)
    
    @property
    def choices(self) ->'list[Course.Course]': 
        """Les choix de l'étudiant
        """
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value

    @property
    def choices_num(self) -> 'list[int]':
        """La liste des num des choix de l'étudiant
        """
        choices_num = []
        for i in self.choices:
            choices_num.append(i.num)
        return choices_num

    @property
    def choices_remaining(self) ->'list[Course.Course]': 
        """La liste des choix restants de l'étudiant
        """
        return self._choices_ramaining

    @choices_remaining.setter
    def choices_remaining(self, value):
        self._choices_ramaining = value

    @property
    def choices_remaining_num(self) -> List[int]:
        """La list des num de choix restants de l'étudiant
        """
        num = []
        for i in self.choices_remaining:
            num.append(i.num)
        return num

    @property
    def nbr_remaining_choices(self) -> int:
        """Le nombre de choix restants de l'étudiant
        """
        return len(self.choices_remaining)

    @property
    def courses(self) ->'list[Course.Course]':
        """Les cours attribués à l'étudiant
        """
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value

    @property
    def courses_num(self) ->'list[int]':
        """La liste des num des cours attribués à l'étudiant
        """
        courses_num = []
        for i in self.courses:
            courses_num.append(i.num)
        return courses_num

    @property
    def nbr_courses_chosen(self) -> int:
        """Le nombre de cous attribués à l'étudiant
        """
        return len(self.courses)

    @property
    def num(self) -> int:
        """Le numéro de l'étudiant
        """
        return self._num
    
    @property
    def satisfaction_value(self) -> float:
        """La satisfaction de l'étudiant
        """
        satisfaction = 0
        for course in self.courses:
            index = self.choices.index(course)
            satisfaction += self._satisfaction_list[index]
        for i in range (self._nbr_courses - self.nbr_courses_chosen):
            index = self.choices.index(self.choices_remaining[i])
            satisfaction += self._satisfaction_list[index]
        return satisfaction / self._nbr_courses

    @property
    def nbr_courses(self):
        """Le nombre de cours que doit choisir l'étudiant
        """
        return self._nbr_courses

    @property
    def nbr_choices(self):
        """Le nombre de choix de l'étudiant
        """
        return self._nbr_choices
    def __str__(self):
        return "\nStudent " + str(self.num) + " :\n    Choices : " + str(self.choices_num)+ "\n    Remainig choices : " + str(self.choices_remaining_num) + "\n    Courses : " + str(self.courses_num) + "\n    Satisfaction : " + str(self.satisfaction_value) + "%"

    def __repr__(self):
        return str(self)
    
    def __lt__(self,other : Self):
        return self.nbr_remaining_choices + self.nbr_courses_chosen < other.nbr_remaining_choices + other.nbr_courses_chosen


    def choose_courses(self, courses : list, nbr : int) -> 'list[Course.Course]':
        """Crée la liste des choix de l'étudiant

        Args:
            courses (list): La liste des possibilités de cours
            nbr (int): le nombre de cours que doit choisir l'étudiant

        Returns:
            list[Course.Course]: la liste des cours choisis
        """
        for i in range (nbr):
            choice = random.choice(courses)
            choice.students_choice.append(self)
            self.choices.append(choice)
            courses.remove(choice)

    def assign_course(self, course : Course) -> Tuple[bool, bool]:
        """Assigne un cours à l'étudiant

        Args:
            course (Course): Le cours assigné à l'étudiant

        Returns:
            Tuple[bool, bool]: bool0 : True si l'étudiant a tous ses cours, False sinon
                               bool1 : True si le cours est complet, False sinon
        """
        result = [False, False]
        self.courses.append(course)
        course.students.append(self)
        course.students_choice.remove(self)
        self.choices_remaining.remove(course)
        if self.nbr_courses_chosen == self._nbr_courses:
           result[0] = True
        if len(course.students) == course.places:
            result[1] = True
        return result
    
    def create_satisfaction_list(self, nbr_choices : int, nbr_courses : int) -> 'list[int]':
        """Crée la liste de satisfaction de l'étudiant. Elle attribue une note aux cours en fonction de la position dans les choix de l'étudiant

        Args:
            nbr_choices (int): le nombre de choix de l'étudiant
            nbr_courses (int): le nombre de cours qu'il doit suivre

        Returns:
            list[int]: la liste de satisfacion
        """
        satisfaction_list = []
        step = 20
        satisfaction = 100
        for i in range (nbr_courses):
            satisfaction_list.append(satisfaction)
        satisfaction -= step
        for i in range (nbr_courses, nbr_choices):
            satisfaction_list.append(satisfaction)
            satisfaction -= step
        return satisfaction_list

