import ProjectSolved
import Student
import random

def fixSolution(projects, students) :
    projectsToFix = []
    studentsToFix = []

    #find students with too much courses
    for student in students :
        if studentHasTooMuchCourses(student):
            studentsToFix.append(student)

    #fix Students
    for studentToFix in studentsToFix :

        for course in studentToFix._courses :
            if isProjectToFix(course) :
                removeStudentFromProject(studentToFix, course)
        
        while studentHasTooMuchCourses(studentToFix) :
            removeStudentFromProject(studentToFix, studentToFix.courses(len(studentToFix._courses)-1))

    #find projects to fix
    for project in projects :
        if isProjectToFix(project) :
            projectsToFix.append(project)

    #fix project
    for projectToFix in projectsToFix :
        #remove students with too much courses
        for student in project.students :
            if isStudentToFix(student) :
                removeStudentFromProject(student, projectToFix)
        
        #remove randomly some student
        studentsToMove = len(project.students) - project.room
        while(studentsToMove > 0) :
            studentToRemove = projectToFix.students[random.randint(0, len(project.students))]
            removeStudentFromProject(studentToRemove, projectToFix)
            studentsToMove = len(project.students) - project.room

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
            
        """
        good_choices = []
        for project in projects :
            if not isProjectToFix(project) :
                good_choices.append(project)
        
        
        for good_choice in good_choices :
            if studentHasNotEnoughCourses(studentToFix) :
                studentToFix.assign_course(good_choice)
        """


def isProjectToFix(project) :
    if len(project.students) > project.room :
        return True
    return False

def isCourseToFix(course) :
    if len(course._student) > course._places :
        return True
    return False

def isProjectFull(project) :
    if len(project.students) < project.room :
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

def removeStudentFromProject(student, project) :
    project.students.remove(student)
    student.couses.remove(project)



