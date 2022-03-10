from Instance.Course import Course
from Instance.Student import Student


class Instance:
    _student = []
    _courses = []

    def __init__(self, nbr_students, nbr_courses, nbr_courses_by_student):
        self.create_courses(nbr_courses)
        self.create_students(nbr_students, nbr_courses_by_student)


    @property
    def student(self):
        return self._student
    
    @student.setter
    def student(self, value):
        self._student = value

    @property
    def courses(self):
        return self._courses
    
    @courses.setter
    def courses(self, value):
        self._courses = value

    def __str__(self):
        return "Instance :\n" + str(self._courses) + str(self._student)

    
    def create_courses(self, nbr_courses):
        for i in range(nbr_courses):
            self.courses.append(Course(i))

    def create_students(self, nbr_students, nbr_courses_by_student):
        for i in range (nbr_students):
            self.student.append(Student(i,self.courses, nbr_courses_by_student))