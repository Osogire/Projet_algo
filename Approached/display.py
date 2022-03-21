import ProjectSolved

def interface(projects :ProjectSolved, fileName, students, studentID, w, options):
    '''
    Interfaces the results of the division of projects by students

    :param projects: list of the projects
    :param fileName: name of the file to save the results
    :param studentID: list of name of students
    :param w: options of students

    :type projects: class Project
    :type fileName: String 
    :type studentID: table of String
    :type w: dictionary of {(student, project) : integer}


    :return files: the display in files saved 
    '''
    # If a project does not have a student display nothing
    studentID.append(" ")

    # Boolean allowing to quit the program
    getOut = False
    while(not getOut):
        # Display allowing the user to choose what he wants to display
        print("\nSi vous voulez voir le nombre d'étudiants pour chaque projet, appuyez sur A")
        print("Si vous voulez voir le nom des étudiants pour tous les projets, appuyez sur Z")
        print("Si vous voulez voir le nombre d'étudiants pour un projet particulier, appuyez sur E")
        print("Si vous voulez voir le taux de satisfaction, appuyez sur R")
        print("Si vous voulez quitter, appuyer sur Q")

        # Get the choice of the user
        value = input()

        # Display and save the number of student per project
        if (value == 'A' or value == 'a'):
            fileNbStudent = open(fileName + "nbStudent.txt","w")
            fileNbStudent.write("------------ Résultat ------------")
            for projet in projects:
                if(len(projet.students) == 1):
                    print("Pour le projet " + str(projet.id) + " il y n'y a pas d'étudiant pour " + str(projet.room) + " places prévues\n")
                    fileNbStudent.write("\nProjet " + str(projet.id) + " : 0 étudiant/" + str(projet.room) + "\n")
                else:
                    print("Pour le projet " + str(projet.id) + " il y a " + str(len(projet.students)) + " étudiants pour " + str(projet.room) + " places prévues\n")
                    fileNbStudent.write("\nProjet " + str(projet.id) + " : " + str(len(projet.students)) + " étudiants/" + str(projet.room) + "\n")
            fileNbStudent.close()
            print("Le fichier "+ fileName + "nbStudent.txt a été créé")
            
        # Display the name of the students for each projects      
        elif (value == 'Z' or value == 'z'):
            nb = 0
            fileAll = open(fileName + "all.txt","w")
            fileAll.write("------------ Résultat ------------\n")
            # Write the number of the projet in the console and in the file
            for projet in projects :
                fileAll.write("\n\nPour le projet " + str(projet.id) + " (" + str(len(projet.students)) + "/" + str(projet.room) + ")")
                print("Pour le projet " + str(projet.id)+ " (" + str(len(projet.students)) + "/" + str(projet.room) + ")")
                nb += len(projet.students)
                # Write the students for each projects
                for student in projet.students:
                    fileAll.write( "\n   étudiant : " + str(student)+ " => " + studentID[student])
                    print("   étudiant : " + str(student) + " => " + studentID[student])
            fileAll.close()
            print("Le fichier " + fileName + "all.txt a été créé")
            print("au total :" + str(nb))


        # Allow the user to print the information of one particular project
        elif (value == 'E' or value == 'e'):
            # Ask to choose one particular project
            print("Veuillez entrer le numéro du projet pour lequel vous voulez la liste des étudiants\n")
            nProject = input()
            # Write in the console the information for one specific project
            for projet in projects:
                if(projet.id == int(nProject)):
                    print("Pour le projet " + str(projet.id) + " il y a " + str(len(projet.students)) + " étudiants+/" + str(projet.room))
                    # Write in the consol the students for this project
                    for student in projet.students:
                        print("   étudiant : " + str(student) + " => " + studentID[student])
                    
        # If the user wants to quit, getOut is put to True
        elif(value == 'Q' or value == 'q'):
            getOut = True

        # If the user wants the info of the satisfaction of the students
        elif(value == 'R' or value == 'r'):
            tabSatisfation = calculateProba(projects, students, w, options)
            i = 0
            for pourcentage in tabSatisfation:
                i += 1
                # Display the pourcentage of students for each options
                print("Pour l'option " + str(i) + " : " + str(pourcentage) + "%")


        # If the choice does not correspond to a possibility ask to choose again
        else:
            print("Le choix que vous avez fait n'existe pas, Veuillez recommencer\n")


def calculateProba(projects : ProjectSolved, students, w, options):
    '''
    Calculate the different distributions of students for each options

    :param projects: list of the projects
    :param students: list of the students with the options
    :param w: options of students

    :type projects: class Porject
    :type students: table of Student
    :type w: dictionary of {(student, project) : integer}

    :return files: the display in files saved 
    '''
    # Initialisation of the number of student by options 
    optionNb = []
    for i in range(len(options)):
        optionNb.append(0)
    # For each student by projects count the number of student who have the option
    for pr in projects :
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