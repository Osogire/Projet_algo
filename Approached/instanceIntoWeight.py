def getWeigthedOptions(students, nbCourses, option_weights):
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

    for student in students:
        for j in range(nbCourses):
            w[(student.num, j)] = option_weights[len(option_weights) - 1]
        for j in range(len(option_weights) - 1):
            w[(student.num, student.choices[j].num)] = option_weights[j]

    return w


def getWeightsDistributedInRange(numberOfWeights: int, minWeight: int, maxWeight: int, step: float) -> [int]:
    """
    return list of weights destributed by function    x -> (max-min)*setp^x+min
    :param numberOfWeights:
    :param minWeight:
    :param maxWeight:
    :param step:
    :return:
    """
    rangeOfWeight = maxWeight - minWeight
    weightTab = []
    for i in range(0, numberOfWeights):
        weightTab.append(int(rangeOfWeight * pow(step, i) + minWeight))
    return list(reversed(weightTab))
