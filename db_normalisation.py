from .db_connection_level_0 import get_connection

def normalized_city():
    conn = get_connection()

    cur = conn.cursor()

    result =  cur.executescript(
        """
        drop table if exists Record_Normalized;
        drop table if exists City;

        create table if not exists City(city_id integer primary key autoincrement, city_name text unique not null);

        Insert into City(city_name)
        select distinct city from Record;

        create table if not exists Record_Normalized(
        id integer primary key, 
        name text, age integer, 
        city_id integer, 
        score real, 
        foreign key (city_id) references City(city_id)
        );

        Insert into Record_Normalized(id, name, age, city_id, score)
        select record.id, record.name, record.age, City.city_id, record.score
        from Record
        Inner join City
        on record.city = City.city_name
        """
    )

    conn.commit()
    conn.close()

    return result


normalized_city()
