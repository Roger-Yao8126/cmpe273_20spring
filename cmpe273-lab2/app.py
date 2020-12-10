# use json
from flask import Flask, escape, request

app = Flask(__name__)

DB = {"students": [],
      "classes": []
      }


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


studentId = 1234456
# Student POST
@app.route('/students', methods=['POST'])
def create_student():
    req = request.json
    studentName = req["name"]
    global studentId
    studentInfo = {
        "id": studentId,
        "name": studentName
    }
    DB["students"].append(studentInfo)
    studentId = studentId + 1
    return studentInfo, 201

# Student GET
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    for s in DB["students"]:
        if s['id'] == int(id):
            return s, 201
    return "Student not found", 201


# class POST
classId = 1122334
@app.route('/classes', methods=['POST'])
def create_class():
    global classId
    req = request.json
    className = req["name"]
    classInfo = {
        "id": classId,
        "name": className,
        "students": []
    }
    DB["classes"].append(classInfo)
    classId = classId + 1
    return classInfo, 201

# class GET Session
@app.route('/classes/<id>', methods=['GET'])
def get_class(id):
    for c in DB["classes"]:
        if c["id"] == int(id):
            return c, 201
    return "Class not found", 201

# Patch: Add student to a class
@app.route('/classes/<int:classId>', methods=['PATCH'])
def add_student(classId):
    req = request.json
    studentId = req["student_id"]
    studentInfo = {}
    # get student info
    for s in DB["students"]:
        if s['id'] == int(studentId):
            studentInfo = s
            break
        return "Student not found", 201
    # locate class in DB and patch

    for i in range(len(DB["classes"])):
        if DB["classes"][i]["id"] == classId:
            DB["classes"][i]["students"].append(studentInfo)
            return DB["classes"][i]
        else:
            return "Class not found"
    return abort(404)


@app.route('/printall')
def printall():
    return DB


if __name__ == "__main__":
    app.run(debug=True)
