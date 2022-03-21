class ProjectSolved:
    '''
    Project class corresponding to the project divided by student according to their choices 

    :member id: identifiant of the project
    :member students: list of the students for this project
    :member room: room planned for this project
    '''
    # Initialisation of the list of student
    students = []

    # Room planned for the project
    room = 0

    # Initialisation of the id and the list of student for the instance of the project
    def __init__(self, id, students, room):
        self.id = id
        self.students = students
        self.room = room 