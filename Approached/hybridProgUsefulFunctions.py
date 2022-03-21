import operator

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

def getListOfStudent(n_students):
    '''
    Get the list of student

    :param n_students: number of the students
    :type n_students: integer

    :return students: list of students
    :rtype students: list of integer
    '''
    students = []
    for i in range(n_students):
        students.append(i)

    return students


def roomWithCoeff(rooms, coeff):
    '''
    Add a coefficient to a list of room

    :param rooms: list of rooms
    :param coeff: coefficient to multiply each element of the list

    :type rooms: list of integer
    :type coeff: integer

    :return roomCoeffed: list of room with coefficient
    :rtype roomCoeffed: list of integer
    '''
    roomCoeffed = []
    for room in rooms:
        roomCoeffed.append(room * coeff)
    return roomCoeffed

def getIndex(student_index, project_index, n_projects):
    '''
    Get the index of the matrix corresponding to the index of students and projects
    (opposite of getStudentAndProject)

    :param student_index: index of the student
    :param project_index: index of the project
    :param n_projects: number of projects

    :type student_index: integer
    :type project_index: integer
    :type n_projects: integer

    :return index: index corresponding to project_student
    :rtype students: integer
    '''
    return student_index * n_projects + project_index

def getStudentAndProject(index, n_projects):
    '''
    Get the indexes of the matrix corresponding to the index of students and projects
    (opposite of get_index)

    :param index: index of the project_student
    :param n_projects: number of projects

    :type index: integer
    :type n_projects: integer

    :return (student_index, project_index): index corresponding to project_student
    :rtype (student_index, project_index): tuple of integers
    '''
    return divmod(index, n_projects)


def getProjectsSolvedFromSched(n_projects, tmpProjects, room):
    '''
    Get the projects from a list

    :param n_projects: number of projects
    :param tmpProjects: dictionnary of project not sorted
    :param room: list of number of student allowed per project

    :type n_projects: integer
    :type tmpProjects: dictionnary
    :type room: list of integer

    :return projects: dictionnary of projects associated to students
    :rtype projects: dictionnary of integers
    '''
    for k in range(n_projects):
        if k not in tmpProjects:
            tmpProjects[k] = [-1]

    # Sort the table of project
    sortedTableOfProjects = sorted(tmpProjects.items(), key=operator.itemgetter(0))

    # Create a table of Project 
    projects = []
    i = 0
    for project in sortedTableOfProjects:
        projects.append(ProjectSolved(project[0],project[1], room[i]))
        i += 1
    # Return the table of project
    return projects