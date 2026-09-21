from .db_connection_level_0 import get_connection

def people_from_given_city():
    conn = get_connection()
    cur = conn.cursor()

    city = input("Enter the city name: ")

    result =  cur.execute(
        """
        Seleet *from Record where city = ?
        """,
        (city,)
    ).fetchall()

    conn.close()
    return result
    

def people_above_given_score():
    conn = get_connection()
    cur = conn.cursor()

    score = float(input("Enter the score: "))

    result =  cur.execute(
        """
        Select *from Record where score > ?
        """,
        (score,)
    ).fetchall()


def top_5_highest_score():
    conn = get_connection()
    cur = conn.cursor()

    result =  cur.execute(
        """
        Select *from Record order by score desc limit 5
        """
    ).fetchall()

    return result

def people_sorted_by_age():
    conn = get_connection()
    cur = conn.cursor()

    result =  cur.execute(
        """
        Select *from Record order by age 
        """
    ).fetchall()

    return result

data = top_5_highest_score()
print(data)

