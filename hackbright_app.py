import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    print "Successfully added project: %s %s %s"%(title, description, max_grade)

def give_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?,?,?)"""
    DB.execute(query, (student_github, project_title, grade))

    CONN.commit()
    print "Successfully added grade %r for Project %s for Student %s"%(grade, project_title, student_github)

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project: %s   
Description: %s
Max. Grade: %s """ %(row[0], row[1], row[2])

def get_grade_by_project(github, title):
    query = """SELECT * FROM Grades WHERE project_title = ? and student_github = ?"""
    DB.execute(query, (title, github))
    row = DB.fetchone()
    print """\
Student Github: %s
Project: %s
Grade: %r""" % (row[0], row[1], row[2])

def get_grades_by_student(github):
    query = """SELECT * FROM Grades WHERE student_github= ?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    for item in row:
        print """\
        Project: %s
        Grade: %d""" %(item[1], item[2])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(' ',1)
        command = tokens[0]
        args = tokens[1].split(',')

        # print "%r" % args
        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_search":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "student_project_grade":
            get_grade_by_project(*args)
        elif command == "give_grade":
            give_grade(*args)
        elif command == "get_grades_by_student":
            get_grades_by_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
