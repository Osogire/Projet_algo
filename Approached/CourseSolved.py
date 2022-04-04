class CourseSolved:
    '''
    Course class corresponding to the course divided by student according to their choices 

    :member id: identifiant of the course
    :member students: list of the students for this course
    :member room: room planned for this course
    '''
    # Initialisation of the list of student
    students = []

    # Room planned for the course
    room = 0

    # Initialisation of the id and the list of student for the instance of the course
    def __init__(self, id, students, room):
        self.id = id
        self.students = students
        self.room = room 