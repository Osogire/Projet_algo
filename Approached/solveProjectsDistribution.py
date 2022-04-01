import readSolution
import fromExcelToPython
import findSolution
import lp
import random


def getOptionsFromXLS(students, nbCourses):
    '''
    Get choices of students from the choices made in the XLS file

    :param students: list of students
    :param nbCourses: number of courses

    :type students: list of integers
    :type nbCourses: integer

    :return w: options of the students
    :rtype w: dictionnary {(student, course) : weight  of options}
    '''
    w = {}
    o1 = -10000
    o2 = -8000
    o3 = -5000
    o4 = -2000
    o5 = -500
    o6 = 100000
    '''
    o1 = -10000
    o2 = -5000
    o3 = -1000
    o4 = -500
    o5 = -10
    o6 = 100000'''
    for student in students:
        for j in range(int(nbCourses)):
            w[(student.id, j)] = o6

        w[(student.id, student.option1)] = o1
        w[(student.id, student.option2)] = o2
        w[(student.id, student.option3)] = o3
        w[(student.id, student.option4)] = o4
        w[(student.id, student.option5)] = o5
    return w

# Main program to solve the distribution of course in function of a llist of students who emitted 5 options

print("-------------------------------------------------------------------------------")
print("|                                 Bienvenue                                    |")
print("-------------------------------------------------------------------------------\n")

print("Ce programme a pour but de résoudre le problème de répartition des courses à partir des choix d'étudiants sous format xls")

print("\n----------------- Etape 1 : Récupération des données -------------------")

# Get the number of courses
print("Entrez le nombre de courses :")
nbCourses = input()

# Get the number of students 
print("Entrez le nombre d'étudiants :")
nbStudents = input()

# CHANGE THE PATH HERE
[students, studentID] = fromExcelToPython.getStudentsFromXls("C:/Users/Jimmy/Desktop/julia/studentsCHoices.xls", int(nbCourses), int(nbStudents))

# Boolean to get out the interface
itsOK = True

while(itsOK):
    courses = []

    typeOk = True
        
    if(type(nbCourses) == type(1)):
        typeOk = False

    # Get the room for each courses
    print("\nEntrez le nombre de place par course :")

    # Ask the user if he wants to fill the number of student per course or use the value written in the program
    print("Voulez-vous renseigner le nombre d'étudiants par courses individuellement ? (y/n)")
    wantToWrite = input()

    # Ask the number of student per course individually
    if wantToWrite == 'y' or wantToWrite == 'Y':
        for cr in range(int(nbCourses)):
            print("Pour le course " + str(cr) + ": ")
            nbStudent = input()
            courses.append(lp.Project(cr, nbStudent))

    # Fill the number of student per course with the table above (nbStudentPerCourse)
    else:
        nbStudentPerCourse = [4, 5, 2, 4, 5, 6, 6, 4, 5, 4, 6, 4, 2, 5, 3, 4, 6, 6, 6, 6, 5, 4, 6, 4, 4, 4, 6, 4, 6, 8, 6, 6, 4, 6, 4, 5, 5, 4, 6]
        for cr in range(int(nbCourses)):
            courses.append(lp.Project(cr, nbStudentPerCourse[cr]))

    

    # Construct the model from the list of students and courses
    model = lp.Model(students, courses)

    # Allow the user to check if the model corresponds to what he expected
    print("Voici le modèle que vous avez entré :\n")
    lp.printModel(model)

    get = True

    # Ask the user to re enter the values
    while(get):
        print("Vous convient-il ? (y/n)")
        good = input()

        if(good == 'y' or good == 'Y'):
            itsOK = False
            get = False
        elif(good == 'n' or good == 'N'):
            itsOK = True
            get = False
        else:
            print("Votre input n'est pas correct")
    
print("\n----------------- Etape 2 : Création du fichier Linear Program -------------------")

# Generate the lp file corresponding to the model and get its name
fileLp = lp.lp(model, "lpFileGenerated")

fileLpE = fileLp + '.lp'

print("\n----------------- Etape 3 : Calcul de la solution avec glpk -------------------")

# Calculate the solution with glpk
solution = findSolution.findSolution(fileLpE, "solutionGLPK.txt")

print("\n----------------- Etape 4 : Récupération de la solution -------------------")

# Read the solutions and get the distribution of students for each course
courses2 = readSolution.readSolution(solution, nbStudents, nbCourses, nbStudentPerCourse)

print("\n----------------- Etape 5 : Lecture des résultats -------------------")

# Ask the user the name of the file to save
print("Entrez le nom du fichier à exporter :")
fileName = input()

# Interface the results and generate the results into files 
readSolution.interface(courses2, fileName, students, studentID, getOptionsFromXLS(students, nbCourses), nbStudentPerCourse)
 
