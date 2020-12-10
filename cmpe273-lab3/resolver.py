import json
students = []
classes = []


def getStudents(_, info, id):
    for student in students:
        if student['id'] == id:
            return student


def getClasses(_, info, id):
    for c in classes:
        if c['id'] == id:
            return c


firstSid = 0


def createStudent(_, info, name):
    if len(students) == 0:
        studentId = firstSid
    else:
        studentId = students[-1]['id'] + 1
    student = {
        'id': studentId,
        'name': name
    }
    students.append(student)
    return student


firstCid = 101


def createClass(_, info, name):
    if len(classes) == 0:
        classId = firstCid
    else:
        classId = classes[-1]['id'] + 1
    newClass = {
        'id': classId,
        'name': name,
        'students': []
    }
    classes.append(newClass)
    return newClass


def addStudentInClass(_, info, classId, studentId):
    try:
        for student in students:
            if student['id'] == studentId:
                break
    except TypeError:
        return "Student Not Found"
    try:
        for c in classes:
            if c['id'] == classId:
                c['students'].append(student)
                break
    except TypeError:
        return "Class Not Found"
    return c
