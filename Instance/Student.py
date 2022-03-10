import copy
import random

from Instance.Course import Course




class Student:

    _num = 0
    _choices = []
    _courses = []
    
    def __init__(self, num):
        self._num = num
        self._choices = []
        self._courses = []

    def __init__(self, num, courses, nbr_courses):
        self._num = num
        self.choices = self.choose_courses(copy.deepcopy(courses), nbr_courses)

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        self._choices = value

    @property
    def courses(self):
        return self._courses

    @courses.setter
    def courses(self, value):
        self._courses = value

    @property
    def num(self):
        return self._num
    
    def __str__(self):
        return "\nStudent " + str(self.num) + " :\nChoices :\n" + str(self.choices) + "\nCourses :\n" + str(self.courses)

    def __repr__(self):
        return str(self)


    def choose_courses(self, courses : list, nbr_courses):
        choices=[]
        for i in range (nbr_courses):
            choice = random.choice(courses)
            choices.append(choice.num)
            courses.remove(choice)
        return choices