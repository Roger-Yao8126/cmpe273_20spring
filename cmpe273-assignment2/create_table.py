from flask import Flask, escape, request
import sqlite3

conn = sqlite3.connect('test.db')

# sqlite3 cursor class
c = conn.cursor()

c.execute("""DROP TABLE IF Exists test_subject""")
c.execute("""DROP TABLE IF Exists test_answer""")
c.execute("""DROP TABLE IF Exists scantron""")
c.execute("""DROP TABLE IF Exists result""")

c.execute("""CREATE TABLE test_subject(
            test_id INTEGER,
            subject VARCHAR(20),
            PRIMARY key(test_id)
)""")

c.execute("""CREATE TABLE test_answer(
            test_id INTEGER,
            question_id VARCHAR[3],    
            answer CHAR(1)
)""")

c.execute("""CREATE TABLE scantron(
            scantron_id INTEGER,
            scantron_url VARCHAR(30),
            name VARCHAR(20),
            subject  VARCHAR(20),
            score INT
)""")

c.execute("""CREATE TABLE result(
            scantron_id INTEGER,
            subject VARCHAR(20),
            question_id VARCHAR[3],
            actual CHAR(1)
)""")

conn.commit()
conn.close()