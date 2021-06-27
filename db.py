import sqlite3

connect = sqlite3.connect('ssis.db')
cursor = connect.cursor()


def ssisdb():
    # initiate or connects data base

    connect = sqlite3.connect('ssis.db')
    cursor = connect.cursor()
    # create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "course"(
        course_id VARCHAR(4) NOT NULL,
        course VARCHAR(50) NOT NULL,
        PRIMARY KEY(course_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "student"(
        student_id TEXT NOT NULL,
        name TEXT   NOT NULL,
        gender  TEXT NOT NULL,
        year_level TEXT NOT NULL,
        course_id TEXT NOT NULL,
        PRIMARY KEY(student_id),
        FOREIGN KEY(course_id) REFERENCES course(course_id)
        );
    """)

    connect.close()

    return 0


# select = '2019-0001'

# cursor.execute('DELETE from student WHERE student_id = (?)', (select,))

# cursor.execute("SELECT* FROM student WHERE student_id = '2019-0608'")
# print(cursor.fetchall())


def add_rows():
    students = [('2019-0608', 'John Eric Engana', 'M', '2nd Year', 'BSCS'),
                ('2019-0001', 'John Eric Engana', 'M', '2nd Year', 'BSCS'),
                ('2019-0002', 'John Eric Engana', 'M', '2nd Year', 'BSCS'),
                ('2020-0003', 'John Eric Engana', 'M', '1st Year', 'BSIT')]
    cursor.executemany("INSERT INTO student VALUES(?,?,?,?,?)", students)


def add_course():
    course = [('BSCS', 'Bachelor of Computer Science'),
              ('BSIS', 'Bachelor of Information Studies'),
              ('BSCA', 'Bachelor of Computer Applications'),
              ('BSIT', 'Bachelor of Information Technology')]
    cursor.executemany("INSERT INTO course VALUES(?,?)", course)


cursor.execute("SELECT* FROM course")
print(cursor.fetchall())
connect.commit()
connect.close()
