# use json.
# seems click the run button cuase problem. type "python3 upload.py" at terminal
from flask import Flask, escape, request
import sqlite3
import json

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

test_id = 1
@app.route('/api/tests', methods=['POST'])
def create_test():
    req = request.json
    subject = req["subject"]
    answer_keys = req["answer_keys"]
    global test_id

    testInfo = {
        "test_id": test_id,
        "subject": subject,
        "answer_keys": answer_keys,
        "submission": []
    }
    conn = sqlite3.connect('test.db')
    # sqlite3 cursor class
    c = conn.cursor()
    c.execute("INSERT INTO test_subject VALUES(:test_id, :subject) ",
              {'test_id': str(test_id), 'subject': subject})
    for key, value in answer_keys.items():
        c.execute("INSERT INTO test_answer VALUES(:test_id,:question_id,:answer) ",
                  {'test_id': str(test_id), 'question_id': key, 'answer': value})
    conn.commit()
    conn.close()
    test_id = test_id + 1
    return testInfo, 201


# upload a scantron
@app.route('/api/tests/<int:test_id>/scantrons', methods=['POST'])
def scantrons(test_id):
    f = request.files['data']
    fname = f.filename
    print("filename >>>" + fname)

    ## assuming all the scantron json file having name like "scantron-<scantron_id>.json"
    indexofsuffix = fname.index(".json")
    scanId = fname[9:indexofsuffix]
    try:
        scantron_id = int(scanId)
    except ValueError:
        print("Unable to get scantron ID from fileName, use the right format as  scantron-<scantron_id>.json")
    file = f.read()
    scantron = json.loads(file)
    name = scantron['name']
    scantron_url= "http://localhost:5000/files/scantron-" + str(scantron_id)+".json"
    subject = scantron['subject']
    answer_keys =scantron['answers']
    conn = sqlite3.connect('test.db')
    # sqlite3 cursor class
    c = conn.cursor()
    result = {}
    score = 0
    c.execute("SELECT test_id FROM test_subject WHERE subject =:subject",
              {'subject': subject})
    if (test_id != c.fetchone()[0]):
        print("test_id from weblink doesn't match subject name, please check. ")

    for key, value in answer_keys.items():
        c.execute("SELECT answer FROM test_answer WHERE test_id =:test_id AND question_id =:question_id",
                  {'test_id': test_id, 'question_id': key})
        answerOne = c.fetchone()[0]
        c.execute("INSERT INTO result VALUES(:scantron_id, :subject, :question_id, :actual) ",
                  {'scantron_id': scantron_id, 'subject': subject, 'question_id': key, 'actual': value})
        compare = {
            "actual" : value,
            "expected" : answerOne
        }
        if (value == answerOne):
             score = score+1
        result[key] = compare

    c.execute("INSERT INTO scantron VALUES(:scantron_id, :scantron_url, :name, :subject, :score) ",
              {'scantron_id': scantron_id, 'scantron_url': scantron_url, 'name': name, 'subject': subject, 'score':score})
    scantron = {
        "scantron_id": scantron_id,
        "scantron_url" : scantron_url,
        "name" : name,
        "score": score,
        "result": result
    }
    conn.commit()
    conn.close()
    return scantron,201

# function
def get_result(scantron_id, subject,answer_key):
    conn = sqlite3.connect('test.db')
    # sqlite3 cursor class
    c = conn.cursor()
    c.execute("SELECT question_id, actual FROM result WHERE scantron_id=:scantron_id AND subject =:subject ",
              {'scantron_id':scantron_id, 'subject':subject})
    qid_actual = c.fetchall()
    result= {}
    for actual in qid_actual:
        print("actual[0] >>> ")
        print(actual[0])
        compare = {
                "actual":actual[1],
                "expected":answer_key[actual[0]]
        }
        result[actual[0]]=compare
    return result


@app.route('/api/tests/<int:test_id>', methods=['GET'])
def all_submission(test_id):
    conn = sqlite3.connect('test.db')
    # sqlite3 cursor class
    c = conn.cursor()
    # get test_id and subject pair
    c.execute("SELECT * FROM test_subject")

    c.execute("SELECT * FROM test_subject WHERE test_id =:test_id",{'test_id':test_id})
    subject = c.fetchone()[1]
    print(subject)

    c.execute("SELECT question_id,answer FROM test_answer WHERE test_id =:test_id",{'test_id':test_id})
    answer_total = c.fetchall()
    answer_keys={}
    for pid_answer_One in answer_total:
        print(pid_answer_One[1])
        answer_keys[pid_answer_One[0]]  = pid_answer_One[1]
    print(answer_keys)
    c.execute("SELECT scantron_id,scantron_url,name, score FROM scantron WHERE subject =:subject",{'subject':subject})
    print('fetchall')
    submissions=[]
    scantrons = c.fetchall()
    # build submission
    for scantron in scantrons:
        scantron_id , scantron_url, name, score = scantron
        print(scantron_id)
        print(subject)
        result = get_result(scantron_id,subject,answer_keys)
        submission={
            "scantron_id" :scantron_id,
            "scantron_url" : scantron_url,
            "name" : name,
            "subject":subject,
            "score": score,
            "result": result
        }

        submissions.append(submission)
    print("submissions >>>")
    print(submissions)

    test_all = {
        "test_id": test_id,
        "subject": subject,
        "answer_keys": answer_keys,
        "submissions":submissions
    }
    print("test_all>>>")
    print(test_all)
    conn.commit()
    conn.close()
    return test_all,201

if __name__ == "__main__":
    app.run(debug=True)