import sqlite3

#FIXME RENOVE THE HARDCODED PATH TO CONNECTION

def set_up_all():
    connection = sqlite3.connect(r"C:\Users\aisha\SkillSwap\backend\database.db")
    _set_up_users(connection)
    _set_up_questions(connection)
    _set_up_tags(connection)
    _set_up_questiontags(connection)
    _set_up_tutortags(connection)
    _set_up_questonTutorMatches(connection)
    _set_up_studentTutorMatches(connection)

def _set_up_users(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE IF NOT EXISTS Users 
                           (
                                user_id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                hashed_password TEXT,
                                email TEXT UNIQUE,
                                user_type TEXT CHECK (user_type IN ('student', 'tutor'))
                            )
                            """)

def _set_up_questions(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE Questions 
                           (
                                question_id INTEGER PRIMARY KEY,
                                student_id INTEGER,
                                question_text TEXT,
                                FOREIGN KEY (student_id) REFERENCES Users(user_id)
                            )
                            """)

def _set_up_tags(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE Tags 
                           (
                                tag_id INTEGER PRIMARY KEY,
                                tag_name TEXT
                            )
                            """)

def _set_up_questiontags(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE QuestionTags 
                           (
                                question_id INTEGER,
                                tag_id INTEGER,
                                PRIMARY KEY (question_id, tag_id),
                                FOREIGN KEY (question_id) REFERENCES Questions(question_id),
                                FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
                            )
                            """)

def _set_up_tutortags(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE TutorTags (
                                tutor_id INTEGER,
                                tag_id INTEGER,
                                PRIMARY KEY (tutor_id, tag_id),
                                FOREIGN KEY (tutor_id) REFERENCES Users(user_id),
                                FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
                            )
                            """)
        
def _set_up_questonTutorMatches(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE QustionTutorMatches (
                                match_id INTEGER PRIMARY KEY,
                                tutor_id INTEGER,
                                question_id INTEGER,
                                FOREIGN KEY (tutor_id) REFERENCES Users(user_id),
                                FOREIGN KEY (question_id) REFERENCES Questions(question_id),
                                UNIQUE (tutor_id, question_id)
                                UNIQUE (tutor_id, student_id)
                            )
                            """)

def _set_up_studentTutorMatches(connection: sqlite3.Connection):
    with connection:
        connection.execute("""
                            CREATE TABLE TutorStudentMatches (
                                match_id INTEGER PRIMARY KEY,
                                tutor_id INTEGER,
                                student_id INTEGER,
                                match_date DATE,
                                FOREIGN KEY (tutor_id) REFERENCES Users(user_id),
                                FOREIGN KEY (student_id) REFERENCES Users(user_id),
                                UNIQUE (tutor_id, student_id)
                            )
                            """)