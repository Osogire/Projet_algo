import operator

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
        roomCoeffed.append((room + 1) * coeff)
    return roomCoeffed

def getIndex(student_index, course_index, n_courses):
    '''
    Get the index of the matrix corresponding to the index of students and courses
    (opposite of getStudentAndCourse)

    :param student_index: index of the student
    :param course_index: index of the course
    :param n_courses: number of courses

    :type student_index: integer
    :type course_index: integer
    :type n_courses: integer

    :return index: index corresponding to course_student
    :rtype students: integer
    '''
    return student_index * n_courses + course_index

def getStudentAndCourse(index, n_courses):
    '''
    Get the indexes of the matrix corresponding to the index of students and courses
    (opposite of get_index)

    :param index: index of the course_student
    :param n_courses: number of courses

    :type index: integer
    :type n_courses: integer

    :return (student_index, course_index): index corresponding to course_student
    :rtype (student_index, course_index): tuple of integers
    '''
    return divmod(index, n_courses)


def getCoursesSolvedFromSched(n_courses, tmpCourses, room):
    '''
    Get the courses from a list

    :param n_courses: number of courses
    :param tmpCourses: dictionnary of course not sorted
    :param room: list of number of student allowed per course

    :type n_courses: integer
    :type tmpCourses: dictionnary
    :type room: list of integer

    :return courses: dictionnary of courses associated to students
    :rtype courses: dictionnary of integers
    '''
    for k in range(n_courses):
        if k not in tmpCourses:
            tmpCourses[k] = [-1]

    # Sort the table of course
    sortedTableOfCourses = sorted(tmpCourses.items(), key=operator.itemgetter(0))

    # Create a table of Course 
    courses = []
    i = 0
    for course in sortedTableOfCourses:
        courses.append(CourseSolved(course[0],course[1], room[i]))
        i += 1
    # Return the table of course
    return courses