from .db_connection_level_0 import get_connection

def group_by_people_per_city():

    conn = get_connection()
    cur = conn.cursor()

    result = cur.execute(
            """
            select  city,
            count(id)as [number of people],
            avg(score) as [average score],
            max(Age) as [oldest age]
            from record
            group by city
            """
        ).fetchall()
    conn.close()

    return result

print(group_by_people_per_city())