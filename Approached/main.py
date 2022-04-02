from random import randint
from collections import defaultdict
from dwave.system import LeapHybridSampler, DWaveSampler, EmbeddingComposite
from uuid import uuid1
from dimod import BinaryQuadraticModel
import pandas as pd 
import operator
import time
import CourseSolved
import Student
from display import interface, calculateProba, calculate_statisfaction_rate
from hybridProgUsefulFunctions import *
#from dataFromClassicProgram import room, w, studentsID
from instanceIntoWeight import getWeigthedOptions, getWeightsDistributedInRange
from instance import Instance

#nb etu, nb projets, nb choix, nb_attribué, nb_places
instance = Instance(50, 10, 5, 4, 24)


f = open("savedCurrentInstance.txt", 'w')
f.write(str(instance))    
f.close()
options = getWeightsDistributedInRange(instance.students[0].nbr_courses, -50000,-10000, 0.5)
options += getWeightsDistributedInRange(instance.students[0].nbr_choices - instance.students[0].nbr_courses, 5000,1000, 0.5)
options.append(10000000)
print(options)
w = getWeigthedOptions(instance.students, len(instance._courses), options)
room = []
for i in range(len(instance._courses)):
    room.append(instance.courses[i]._places)

studentsID = []
for i in range(len(instance.students)):
    studentsID.append("Student " + str(i))

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


# --------- BEGIN ---------- #

# Declaration of students and projets  
nbStudents = len(studentsID)
print("Number of students : " + str(nbStudents))


nbCourses = len(room)
print("Number of courses : " + str(nbCourses))


students = getListOfStudent(nbStudents)
courses = getListOfStudent(nbCourses)

size = nbStudents * nbCourses

# coefficient forcing the course to have the number of students needed (helping more the course with more students)
coeff = 1000
roomCoeffed = roomWithCoeff(room, coeff)

# Lagrange parameters
# for the room per courses
lagrange_parameter_room = roomCoeffed

# to force only one course per students
lagrange_parameter_only_one = 100000

# Creation of the matrix
Q = defaultdict(int)

# Objective function
for student_index in students:
    for course_index in courses:
        ind1 = getIndex(student_index, course_index, len(courses))
        Q[(ind1, ind1)] += w[(student_index, course_index)]

# Constraint 2 : Room per courses 
for course_index in courses:
    for student_index in students:
        ind1 = getIndex(student_index, course_index, len(courses))
        Q[(ind1, ind1)] -= (2*(room[course_index]+1) - 1)*lagrange_parameter_room[course_index]


for course_index in courses:
    for student_index in range(len(students)):
        for student_index_2 in range(student_index, len(students)):
            ind1 = getIndex(student_index, course_index, len(courses))
            ind2 = getIndex(student_index_2, course_index, len(courses))
            Q[(ind1, ind2)] += 2*lagrange_parameter_room[course_index]

# Constraint 1 : One course per student
for student_index in students:
    for course_index in courses:
        ind1 = getIndex(student_index, course_index, len(courses))
        Q[(ind1, ind1)] -= (2*instance.students[0].nbr_courses -1)*lagrange_parameter_only_one

for student_index in students:
    for j in range(len(courses)):
        for m in range(j, len(courses)):
            ind1 = getIndex(student_index, j, len(courses))
            ind2 = getIndex(student_index, m, len(courses))
            Q[(ind1, ind2)] += 2*lagrange_parameter_only_one

# Choice of computer
print("\nChoose Hybrid Computer (h) or Quantum Computer (q) : ")
ordi = input() 


if ordi == 'Q' or ordi == 'q':
    print("You chose the quantum D-wave computer\nSending to the d-wave computer...")
    time0 = time.time()
    sampler = EmbeddingComposite(DWaveSampler())
    time1 = time.time()
    results = sampler.sample_qubo(Q,num_reads=5000)
else :
    print("You chose the hybrid D-wave computer\nSending to the d-wave computer...")
    time0 = time.time()
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=0)
    sampler = LeapHybridSampler()
    time1 = time.time()
    results = sampler.sample(bqm, label='TimeStabling')

execTime = time.time() - time1

# Saving the data in a file
print("\nExecution Time (s) : " + str(execTime))
print("Embedding Time (s) : " + str(time1 - time0))
print("Recovery of the results...")
time2 = time.time()
smpl = results.first.sample
energy = results.first.energy
time3 = time.time()
print("Recovery time (s) : " + str(time3 - time2))
print("Total time : " + str(time3 - time0))
print("Size ", size)
print("Energy ", energy)

# Declaration 
resultsFinal = {}

# Get the results in the wanted format
for j in range(size):
    if smpl[j] == 1:
        [student, course] = getStudentAndCourse(j, len(courses))
        if course not in resultsFinal:
            resultsFinal[course] = [student]
        else :
            resultsFinal[course].append(student)



# Get the courses solved
coursesSolved = getCoursesSolvedFromSched(len(courses), resultsFinal, room)

print("\nLe taux de satisfaction globale est de : "+str(calculate_statisfaction_rate(instance, calculateProba(coursesSolved, students, w, options))) + "\n")

# Interface the results
interface(coursesSolved, "results" + str(time.time()), students, studentsID, w, options)


