from math import fabs
from typing import List
#from typing_extensions import Self
#from Student import Student


class Course:

    def __init__(self, num, nbr_places):
        self._student = []
        self._num = num
        self._places = nbr_places
        self._nbr_choosed = 0
        self._student_choice = []

    @property
    def students(self) -> 'list[Student.Student]':
        """La liste d'étudiants suivant le cours
        """
        return self._student

    @students.setter
    def students(self, value):
        self._student = value

    @property
    def student_num(self) ->'list[int]':
        """La liste des num des étudiants suivant le cours
        """
        student_num = []
        for i in self.students:
            student_num.append(i.num)
        return student_num
    
    @property
    def places(self) -> int:
        """le nombre de place du cours
        """
        return self._places
    
    @places.setter
    def places(self,value):
        self._places = value

    @property
    def num(self) -> int:
        """Le num du cours
        """
        return self._num

    @property
    def nbr_student_choice(self) -> int:
        """le nombre d'étudiant ayant comme choix ce cours
        """
        return len(self._student_choice)
    
    @property
    def students_choice(self):
        """Les étudiants ayant choisis ce cours
        """
        return self._student_choice
    
    @students_choice.setter
    def students_choice(self, value):
        self._student_choice = value

    @property
    def students_choice_num(self) -> List[int]:
        """La liste des nume des étudiants ayant choisis ce cours
        """
        num = []
        for i in self.students_choice:
            num.append(i.num)
        return num

    def __str__(self):
        return "\nCourse " + str(self._num) + " :\n    Students : " + str(self.student_num) + "\n    Students choice : " + str(self.students_choice_num)
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        return self.num == other.num