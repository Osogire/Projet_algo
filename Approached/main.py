from random import randint
from collections import defaultdict
from dwave.system import LeapHybridSampler, DWaveSampler, EmbeddingComposite
from uuid import uuid1
from dimod import BinaryQuadraticModel
import pandas as pd 
import operator
import time
import ProjectSolved
import Student
from display import interface, calculateProba
from hybridProgUsefulFunctions import *
#from dataFromClassicProgram import room, w, studentsID
from instanceIntoWeight import getWeigthedOptions
from instanceIntoWeight import getWeightsDistributedInRange
from instance import Instance

instance = Instance(65, 10, 6, 5, 30)
f = open("savedCurrentInstance.txt", 'w')
f.write(str(instance))    
f.close()
#options = [-50000, -10000,-5000,-1000, -10, 100000]
options = getWeightsDistributedInRange(5, -50000,-10, 0.5)
options.append(100000)
print(options)
w = getWeigthedOptions(instance.students, len(instance._courses), options)
room = []
for i in range(len(instance._courses)):
    room.append(38)

studentsID = []
for i in range(len(instance.students)):
    studentsID.append("Student " + str(i))

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


# --------- BEGIN ---------- #

# Declaration of students and projets
nbStudents = len(studentsID) - 1
print("Number of students : " + str(nbStudents))


nbProjects = len(room)
print("Number of projects : " + str(nbProjects))


students = getListOfStudent(nbStudents)
projects = getListOfStudent(nbProjects)

size = nbStudents * nbProjects

# coefficient forcing the project to have the number of students needed (helping more the project with more students)
coeff = 2000
roomCoeffed = roomWithCoeff(room, coeff)

# Lagrange parameters
# for the room per projects
lagrange_parameter_room = roomCoeffed

# to force only one project per students
lagrange_parameter_only_one = 1000

# Creation of the matrix
Q = defaultdict(int)

# Objective function
for student_index in students:
    for project_index in projects:
        ind1 = getIndex(student_index, project_index, len(projects))
        Q[(ind1, ind1)] += 25*w[(student_index, project_index)]

# Constraint 2 : Room per projects => lines 109 and 118 decomment and comment lines 110 & 119 if you don't want to have teh number right on the number of room allowed
for project_index in projects:
    for student_index in students:
        ind1 = getIndex(student_index, project_index, len(projects))
        # Q[(ind1, ind1)] += lagrange_parameter_room[project_index]
        Q[(ind1, ind1)] -= (2*room[project_index])*lagrange_parameter_room[project_index]


for project_index in projects:
    for student_index in range(len(students)):
        for student_index_2 in range(student_index, len(students)):
            ind1 = getIndex(student_index, project_index, len(projects))
            ind2 = getIndex(student_index_2, project_index, len(projects))
            # Q[(ind1, ind2)] += 0
            Q[(ind1, ind2)] += 2*lagrange_parameter_room[project_index]

# Constraint 1 : One project per student
for student_index in students:
    for project_index in projects:
        ind1 = getIndex(student_index, project_index, len(projects))
        Q[(ind1, ind1)] -= lagrange_parameter_only_one

for student_index in students:
    for project_index in projects:
        for project_index_2 in projects:
            ind1 = getIndex(student_index, project_index, len(projects))
            ind2 = getIndex(student_index, project_index_2, len(projects))
            Q[(ind1, ind2)] += lagrange_parameter_only_one*5

# Choice of computer
print("\nChoose Hybrid Computer (h) or Quantum Computer (q) : ")
ordi = input() 

time0 = time.time()

if ordi == 'Q' or ordi == 'q':
    print("You chose the quantum D-wave computer\nSending to the d-wave computer...")
    sampler = EmbeddingComposite(DWaveSampler())
    time1 = time.time()
    results = sampler.sample_qubo(Q,num_reads=5000)
else :
    print("You chose the hybrid D-wave computer\nSending to the d-wave computer...")
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=0)
    sampler = LeapHybridSampler()
    time1 = time.time()
    results = sampler.sample(bqm, label='Example - Nurse Scheduling')

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
    
print("Size ", size)
print("Energy ", energy)
'''
print("\nDo you want to save the data ? (y/n)")
save = input()

if(save == 'y'):
    print("Saving the data...")
    f = open("save" + str(uuid1()) + ".txt", 'w')
    f.write("\nExecution Time : " + str(execTime))
    f.write("\nEmbedding Time : " + str(time0 - time1))
    f.write("\n\tPlaces par projets : ")
    f.write(str(room))
    f.write("\n\tMatrice Q : ")
    f.write(str(Q))

    f.write("\nResults : " + str(smpl))
    f.write("\n\tSize : " + str(size))
    f.write("\n\tEnergy : " + str(energy) )
    f.write("\nResults : \n")
    f.close()
'''
# Declaration 
resultsFinal = {}

# Get the results in the wanted format
for j in range(size):
    if smpl[j] == 1:
        [student, project] = getStudentAndProject(j, len(projects))
        if project not in resultsFinal:
            resultsFinal[project] = [student]
        else :
            resultsFinal[project].append(student)



# Get the projects solved
projectsSolved = getProjectsSolvedFromSched(len(projects), resultsFinal, room)

# Interface the results
interface(projectsSolved, "results" + str(time.time()), students, studentsID, w, options)

