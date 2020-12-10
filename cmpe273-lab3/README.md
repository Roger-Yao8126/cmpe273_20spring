# Lab 3

## Pre-requisites

* Install _Pipenv_

```
pip install pipenv
```

* Install _[Flask](https://palletsprojects.com/p/flask/)_

```
pipenv install flask==1.1.1
```
* Install _[Ariadne](https://ariadnegraphql.org/docs/flask-integration.html)_ for handling GraphQL schema and binding.

```
pipenv install ariadne==0.10.0
```

* Create a schema.py and add this code:

```python
TBD
```

* Create a file called _app.py_ and add this code snippet.

```python
from flask import Flask, escape, request

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
```

* Run your Hello World Flask application from a shell/terminal.

```sh
pipenv shell
$ env FLASK_APP=app.py flask run
```

* Open [this URL](http://127.0.0.1:5000/) in a web browser or run this CLI to see the output.

```
curl -i http://127.0.0.1:5000/
```

## Requirements

You will be building a RESTful class registration API in this lab.

### Domain Model

```
|-------|               |---------|
| Class |* ---------- * | Student |
|-------|               |---------|
```

### GraphQL operations to be implemented.

* Mutate a new student

```
mutation {
createStudent(name:"Bob Smith"){
  id
  name
}
}
```

* Query an existing student

_Request_

```
query {
	getStudents(id:0) {
    name
  }
}
```

_Response_

```
{
    "name" : "Bob Smith"
}
```

* Mutate a class

```
mutation {
createClass(name:"CMPE273"){
  id
  name
}
}
```

* Query a class

```
query {
getClasses(id:101){
  id
  name
  students {
    id
    name
  }
}
}
```

* Add students to a class

```
mutation {
addStudentInClass(classId:101, studentId:2) {
    id
    name
    students {
      id
      name
    }
  
  }
}

```


