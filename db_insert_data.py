from .db_connection_level_0 import get_connection
from python_fundamentals_toolit.tool_kit_level_3 import DataSet
import sqlite3

def create_table():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.executescript(
            """
            Create table if not exists Record(
            id integer primary key, name text, age integer, city text, score real
            );
        """)

        conn.commit()
        conn.close()
    except sqlite3.C as e:
        print(f"database erro: {e}")


def insert_data():
    conn = get_connection()
    cur = conn.cursor()
    filepath = 'python_database_fundamental/messy_people.csv'
    dataset = DataSet(filepath)
    record = dataset.iterate()

    for data in record:

        try:
            if data is not None:
                cur.execute(
                    """
                    Insert into Record
                    values(?, ?, ?, ?, ?)
                    """,
                    (data.id, data.name, data.age, data.city, data.score)
                )

        except sqlite3.IntegrityError:
            print(f"value with {data.id} already exist")

    conn.commit()
    conn.close()

create_table()
insert_data()
