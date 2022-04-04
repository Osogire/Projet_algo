import CourseSolved
import Student
import random

def fixSolution(courses, students) :
    """
    this function helps correcting the solved distribution when a student has too much or not enough courses. And/Or where there is too much student in a course.
    """
    coursesToFix = []
    studentsToFix = []

    #find students with too much courses
    for student in students :
        if studentHasTooMuchCourses(student):
            studentsToFix.append(student)

    #fix Students
    for studentToFix in studentsToFix :

        for course in studentToFix._courses :
            if isCourseToFix(course) :
                removeStudentFromCourse(studentToFix, course)
        
        while studentHasTooMuchCourses(studentToFix) :
            removeStudentFromCourse(studentToFix, studentToFix.courses(len(studentToFix._courses) - 1))

    #find courses to fix
    for course in courses :
        if isCourseToFix(course) :
            coursesToFix.append(course)

    #fix course
    for courseToFix in coursesToFix :
        #remove students with too much courses
        for student in course.students :
            if isStudentToFix(student) :
                removeStudentFromCourse(student, courseToFix)
        
        #remove randomly some student
        studentsToMove = len(course.students) - course.room
        while(studentsToMove > 0) :
            studentToRemove = courseToFix.students[random.randint(0, len(course.students))]
            removeStudentFromCourse(studentToRemove, courseToFix)
            studentsToMove = len(course.students) - course.room

    studentsToFix = []

    #find students with not enough courses
    for student in students :
        if studentHasNotEnoughCourses(student):
            studentsToFix.append(student)

    #fix Students
    for studentToFix in studentsToFix :
        good_choices = []
        for i in range(0,len(studentToFix._choices_ramaining)) :
            if not isCourseToFix(studentToFix._choices_ramaining[i]) :
                good_choices.append(studentToFix._choices_ramaining[i])
        
        for good_choice in good_choices :
            if studentHasNotEnoughCourses(studentToFix) :
                studentToFix.assign_course(good_choice)
            

        good_choices = []
        for course in courses :
            if not isCourseToFix(course) :
                good_choices.append(course)
        
        
        for good_choice in good_choices :
            if studentHasNotEnoughCourses(studentToFix) :
                addStudentInCourse(studentToFix, good_choice)


def isCourseToFix(course) :
    if len(course.student) > course.places :
        return True
    return False

def isCourseFull(course) :
    if len(course.students) < course.room :
        return False
    return True

def isStudentToFix(student) :
    if len(student.courses) != student.nbr_courses :
        return True
    return False

def studentHasTooMuchCourses(student) :
    if len(student.courses) > student.nbr_courses :
        return True
    return False

def studentHasNotEnoughCourses(student) :
    if len(student.courses) < student.nbr_courses :
        return True
    return False

def removeStudentFromCourse(student, course) :
    course.students.remove(student)
    student.courses.remove(course)

def addStudentInCourse(student, course) :
    course.students.append(student)
    student.courses.append(course)



