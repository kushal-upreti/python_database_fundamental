from .db_connection_level_0 import get_connection

def normalized_city():
    conn = get_connection()

    cur = conn.cursor()

    cur.executescript(
        """
        drop table if exists Record_Normalized;
        drop table if exists City;

        create table if not exists City(city_id integer primary key autoincrement, city_name text unique not null);

        create table if not exists Record_Normalized(
        id integer primary key, 
        name text, age integer, 
        city_id integer, 
        score real, 
        foreign key (city_id) references City(city_id)
        );
        """
    )

    city_data= cur.execute(
        """
        select distinct city from Record;
        """
    )
    for data in city_data:
        cur.execute(
            """
            Insert into City(city_name)
            values (?);
            """,
            (data)
        )
    records = cur.execute(
        """
        select record.id, record.name, record.age, City.city_id, record.score
        from Record
        Inner join City
        on record.city = City.city_name
        """
    ).fetchall()

    
    cur.executemany(
        """
        Insert into Record_Normalized(id, name, age, city_id, score)
        values (?, ?, ?, ?, ?);
        """,
        (records)
    )
    conn.commit()
    conn.close()



normalized_city()
