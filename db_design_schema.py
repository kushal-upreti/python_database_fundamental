from .db_connection_level_0 import get_connection
import sqlite3

person_data= [
    (101, "Ram"),
    (102, "Sita"),
    (103, "Hari"),
    (104, "Gita"),
    (105, "Ram"),
    (106, "Krishna"),
    (107, "Sita"),
    (108, "Anil"),
    (109, "Hari"),
    (110, "Ram")
]

subjects_data = [
    (106, "Artificial Intelligence"),
    (101, "Database"),
    (102, "Networking"),
    (104, "Operating Systems"),
    (103, "Python"),
    (105, "Statistics")
]

time_data = [
    (1, "2026-09-16"),
    (2, "2026-09-17"),
    (3, "2026-09-18"),
    (4, "2026-09-19"),
    (5, "2026-09-20"),
    (6, "2026-09-21")
]

exam_data= [
    (101, 101, 1, 85),
    (101, 102, 2, 78),
    (101, 103, 3, 92),
    (102, 101, 1, 74),
    (102, 104, 3, 88),
    (102, 105, 5, 81),
    (102, 106, 6, 90),
    (103, 102, 2, 69),
    (103, 103, 3, 84),
    (103, 106, 5, 76),
    (104, 101, 1, 91),
    (104, 103, 2, 87),
    (104, 104, 4, 79),
    (105, 102, 1, 73),
    (105, 104, 3, 95),
    (105, 105, 5, 82),
    (105, 106, 6, 89),
    (106, 101, 2, 68),
    (106, 102, 3, 77),
    (106, 105, 4, 86),
    (107, 103, 1, 93),
    (107, 104, 3, 71),
    (107, 106, 6, 88),
    (108, 101, 2, 80),
    (108, 102, 4, 75),
    (108, 103, 5, 91),
    (109, 104, 1, 83),
    (109, 105, 3, 79),
    (109, 106, 5, 94),
    (109, 101, 6, 87),
    (110, 102, 1, 72),
    (110, 103, 2, 89),
    (110, 105, 4, 81)
]


def create_table():

    conn= get_connection()
    cur= conn.cursor()
    try:
        result = cur.executescript(
            """
            CREATE TABLE Person(person_id INTEGER PRIMARY KEY, name TEXT NOT NULL);

            CREATE TABLE Exam (
            person_id INTEGER,
            subject_code INTEGER,
            time_id INTEGER,
            score REAL,

            PRIMARY KEY (person_id, subject_code, time_id),

            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (subject_code) REFERENCES Subjects(subject_code),
            FOREIGN KEY (time_id) REFERENCES Time(time_id)
            );

            CREATE TABLE Subjects(
            subject_code INTEGER PRIMARY KEY, 
            subject_name text UNIQUE);

            CREATE TABLE Time(time_id integer primary KEY, exam_date date);

            """
        )

        conn.commit()
        conn.close()
    except sqlite3.OperationalError:
        print('table already exist')

        
def insert_data():

    try:
        conn= get_connection()
        cur= conn.cursor()

        cur.executemany(
            """
            Insert into Person(person_id, name)
            values (?, ?)
            """,
            person_data
        )
        cur.executemany(
            """
            Insert into Subjects(subject_code, subject_name)
            values (?, ?)
            """,
            subjects_data
        )
        cur.executemany(
            """
            Insert into Time(time_id, exam_date)
            values (?, ?)
            """,
            time_data
        )
        cur.executemany(
            """
            Insert into Exam(person_id, subject_code, time_id, score)
            values (?, ?, ?, ?)
            """,
            exam_data
        )

        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        print('data already inserted with this id')



create_table()
insert_data()

def query():
    conn= get_connection()
    cur= conn.cursor()

    query_1 = cur.execute(
        """
        SELECT 
	    Person.person_id,
	    Person.name,
        count(Exam.subject_code) as [number of subject],
        avg(Exam.score) as [average score]
        from Exam
        INNER JOIN Person
        	on Exam.person_id = Person.person_id
        INNER JOIN Subjects
        	on Exam.subject_code = Subjects.subject_code
        INNER JOIN time
        	on Exam.time_id = time.time_id
        GROUP by 
        Person.person_id;
        """
    ).fetchall()

    query_2= cur.execute(
        """
        Select 
        Subjects.subject_code,
        Subjects.subject_name,
        max(Exam.score) as [Best Score]
        from Exam
        Inner Join Subjects
            on Exam.subject_code = Subjects.subject_code
        Group By
        Subjects.subject_code
        """
    ).fetchall()

    conn.close()

    return query_1, query_2


query_1, query_2 = query()

print("\n=== Student Performance ===")
print(f"{'ID':<8} | {'Name':<12} | {'Subjects':<10} | {'Average Score':<15}")
print("-" * 55)

for data in query_1:
    print(f"{data[0]:<8} | {data[1]:<12} | {data[2]:<10} | {data[3]:<15.2f}")

print("\n=== Best Score by Subject ===")
print(f"{'Code':<8} | {'Subject Name':<25} | {'Best Score':<10}")
print("-" * 50)

for data in query_2:
    print(f"{data[0]:<8} | {data[1]:<25} | {data[2]:<10}")
