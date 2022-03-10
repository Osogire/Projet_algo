class Course:
    def __init__(self):
        self._num = 0
        self._student = []
        self._places = 0
    
    def __init__(self, num):
        self._num = num
        self._student = []
        self._places = 0

    @property
    def student(self):
        return self._student

    @student.setter
    def student(self, value):
        self._student = value
    
    @property
    def places(self):
        return self._places
    
    @places.setter
    def places(self,value):
        self._places = value

    @property
    def num(self):
        return self._num

    def __str__(self):
        return "\nCourse " + str(self._num) + " :\nStudents :\n" + str(self.student)
    
    def __repr__(self):
        return str(self)