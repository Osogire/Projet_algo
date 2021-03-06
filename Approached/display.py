import CourseSolved
from instance import Instance
def interface(courses :CourseSolved, fileName, students, studentID, w, options):
    '''
    Interfaces the results of the division of courses by students

    :param courses: list of the courses
    :param fileName: name of the file to save the results
    :param studentID: list of name of students
    :param w: options of students

    :type courses: class Course
    :type fileName: String 
    :type studentID: table of String
    :type w: dictionary of {(student, course) : integer}


    :return files: the display in files saved 
    '''
    # If a course does not have a student display nothing
    studentID.append(" ")

    # Boolean allowing to quit the program
    getOut = False
    while(not getOut):
        # Display allowing the user to choose what he wants to display
        print("\nSi vous voulez voir le nombre d'étudiants pour chaque cours, appuyez sur A")
        print("Si vous voulez voir le nom des étudiants pour tous les cours, appuyez sur Z")
        print("Si vous voulez voir le nombre d'étudiants pour un cours particulier, appuyez sur E")
        print("Si vous voulez voir le taux de satisfaction, appuyez sur R")
        print("Si vous voulez quitter, appuyer sur Q")

        # Get the choice of the user
        value = input()

        # Display and save the number of student per course
        if (value == 'A' or value == 'a'):
            fileNbStudent = open(fileName + "nbStudent.txt","w")
            fileNbStudent.write("------------ Résultat ------------")
            for cours in courses:
                if(len(cours.students) == 1):
                    print("Pour le cours " + str(cours.id) + " il y n'y a pas d'étudiant pour " + str(cours.room) + " places prévues\n")
                    fileNbStudent.write("\nCours " + str(cours.id) + " : 0 étudiant/" + str(cours.room) + "\n")
                else:
                    print("Pour le cours " + str(cours.id) + " il y a " + str(len(cours.students)) + " étudiants pour " + str(cours.room) + " places prévues\n")
                    fileNbStudent.write("\nCours " + str(cours.id) + " : " + str(len(cours.students)) + " étudiants/" + str(cours.room) + "\n")
            fileNbStudent.close()
            print("Le fichier "+ fileName + "nbStudent.txt a été créé")
            
        # Display the name of the students for each courses      
        elif (value == 'Z' or value == 'z'):
            nb = 0
            fileAll = open(fileName + "all.txt","w")
            fileAll.write("------------ Résultat ------------\n")
            # Write the number of the cours in the console and in the file
            for cours in courses :
                fileAll.write("\n\nPour le cours " + str(cours.id) + " (" + str(len(cours.students)) + "/" + str(cours.room) + ")")
                print("Pour le cours " + str(cours.id)+ " (" + str(len(cours.students)) + "/" + str(cours.room) + ")")
                nb += len(cours.students)
                # Write the students for each courses
                for student in cours.students:
                    fileAll.write( "\n   étudiant : " + str(student)+ " => " + studentID[student])
                    print("   étudiant : " + str(student) + " => " + studentID[student])
            fileAll.close()
            print("Le fichier " + fileName + "all.txt a été créé")
            print("au total :" + str(nb))


        # Allow the user to print the information of one particular course
        elif (value == 'E' or value == 'e'):
            # Ask to choose one particular course
            print("Veuillez entrer le numéro du cours pour lequel vous voulez la liste des étudiants\n")
            nCourse = input()
            # Write in the console the information for one specific course
            for cours in courses:
                if(cours.id == int(nCourse)):
                    print("Pour le cours " + str(cours.id) + " il y a " + str(len(cours.students)) + " étudiants+/" + str(cours.room))
                    # Write in the consol the students for this course
                    for student in cours.students:
                        print("   étudiant : " + str(student) + " => " + studentID[student])
                    
        # If the user wants to quit, getOut is put to True
        elif(value == 'Q' or value == 'q'):
            getOut = True

        # If the user wants the info of the satisfaction of the students
        elif(value == 'R' or value == 'r'):
            tabSatisfation = calculateProba(courses, students, w, options)
            i = 0
            for pourcentage in tabSatisfation:
                i += 1
                # Display the pourcentage of students for each options
                print("Pour l'option " + str(i) + " : " + str(pourcentage) + "%")


        # If the choice does not correspond to a possibility ask to choose again
        else:
            print("Le choix que vous avez fait n'existe pas, Veuillez recommencer\n")


def calculateProba(courses : CourseSolved, students, w, options):
    '''
    Calculate the different distributions of students for each options

    :param courses: list of the courses
    :param students: list of the students with the options
    :param w: options of students

    :type courses: class Course
    :type students: table of Student
    :type w: dictionary of {(student, course) : integer}

    :return files: the display in files saved 
    '''
    # Initialisation of the number of student by options 
    optionNb = []
    for i in range(len(options)):
        optionNb.append(0)
    # For each student by courses count the number of student who have the option
    for pr in courses :
        for st in pr.students :
            for stu in students :
                if(st == stu):
                    for i in range(len(options)):
                        # Count for each option
                        if(w[(stu, pr.id)] == options[i]):
                            optionNb[i] += 1
                    
    for i in range(len(options)):
        optionNb[i] = optionNb[i]*100/len(students)

    # Return the pourcentage of student for each options
    return optionNb

def calculate_statisfaction_rate(instance: Instance, probas:[]):
    '''
    Calculate the total satisfaction rate of students after distribution of their courses as done in the exact algorithm

    :param instance: the instance of the problem
    :param probas: distribution of each student for their assignations

    :type courses: class Instance
    :type proba: table of float

    :return files: the total staid=sfaction rate of the students 
    '''
    percentage = []
    for i in range(instance.students[0]._nbr_courses):
        percentage.append(100)
    x = 100
    for i in range(instance.students[0].nbr_choices - instance.students[0]._nbr_courses):
        x -= 20
        percentage.append(x)

    rate = 0
    for i in range(len(percentage)):
        nb_stu_for_choice_i = len(instance.students)*probas[i]/100
        rate += nb_stu_for_choice_i * percentage[i]
    rate = rate/(len(instance.students)*instance.students[0]._nbr_courses)
    return rate 
    