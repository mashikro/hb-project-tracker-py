"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})
    
    row = db_cursor.fetchone()
    # print(row)

    if row is None: #if github doesnt exist fetchone() returns none so row is none
        print('Try again')
        # get_student_by_github(github)

    else:
        print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """


    QUERY = """
        INSERT INTO students (first_name, last_name, github)
        VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})

    db.session.commit()
    print(f"Successfully added student: {first_name} {last_name}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """SELECT title, description, max_grade FROM projects WHERE title = :title
            """

    cursor = db.session.execute(QUERY, {'title': title})
    project_info = cursor.fetchone()

    print(f'The project title is {project_info[0]} and max grade is {project_info[2]} and the description is {project_info[1]}')


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """SELECT grade FROM grades WHERE project_title = :title and student_github = :github
            """
    cursor = db.session.execute(QUERY, {'title': title, 'github': github})
    
    grade = cursor.fetchone()

    print(f'Your grade is {grade[0]}')


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """INSERT INTO grades (student_github, project_title, grade)
    VALUES (:github, :title, :grade)
    """

    db.session.execute(QUERY, {'github': github, 'title': title, 'grade': grade})


    db.session.commit()
    print(f'Assigned a grade for {github} with project {title} a grade of {grade}')

def add_project(title, description, max_grade):
    """Add project details to the project table"""

    sql = '''INSERT INTO projects (title, description, max_grade)
    VALUES (:title, :description, :max_grade)
    '''
    db.session.execute( sql, {
        'title': title,
        'description': description,
        'max_grade': max_grade
        })
    
    db.session.commit()
    print("Added")


def get_grades(github):
    ''' See all the grades for a student'''

    QUERY = '''SELECT grade, project_title 
    FROM grades WHERE student_github = :github
    '''

    cursor = db.session.execute(QUERY, {'github': github})
    grades = cursor.fetchall()

    for project in grades:
        print(f'Project title: {project[1]} and Grade: {project[0]}')

def handle_parameter_error(args, tokens):

    if len(args)+1 != len(tokens):
        print('Number of arguements dont match!')
        

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]
        
        # if len(args) != len(tokens)-1:
        #    raise TypeError(f'{} arguments required')
        # else:
        #     handle_parameter_error(args, tokens)

        if command == "student":
                github = args[0]
                get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_description":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == 'assign_grade':
            github, title, grade =args
            assign_grade(github, title, grade)

        elif command == 'add_project':
            title, description, max_grade = args
            add_project(title, description, max_grade)

        elif command == 'all_grades':
            github = args[0]
            get_grades(github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
