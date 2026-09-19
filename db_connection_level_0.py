import sqlite3

def get_connection():
    conn = sqlite3.connect('python_database_fundamental/people.db')

    return conn

