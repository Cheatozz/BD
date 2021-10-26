import mysql.connector
from mysql.connector import Error
from getpass import getpass


def create_table(conn):
    table_str = '''
    CREATE TABLE games (
        name VARCHAR(50),
        developer_studio VARCHAR(50),
        release_year YEAR(4),
        genre VARCHAR(25)
    )
    PARTITION BY RANGE( release_year ) (
    PARTITION before_2000 VALUES LESS THAN(2000),
    PARTITION before_2010 VALUES LESS THAN(2010),
    PARTITION after_2010 VALUES LESS THAN(MAXVALUE))
    '''
    cursor = conn.cursor()
    cursor.execute(table_str)
    conn.commit()
    print('Table "games" was created\n')
    fill_table(c)


def fill_table(conn):
    fill_in = '''
    INSERT INTO games (name, developer_studio, release_year, genre)
    VALUES
        ("The Elder Scrolls V: Skyrim", "Bethesda Game Studios", 2012, "RPG"),
        ("Disco Elysium", "ZA/UM", 2019, "RPG"),
        ("Wolfenstein 3D", "id Software", 1992, "First-person shooter"),
        ("Tekken", "Namco", 1994, "Fighting"),
        ("Sid Meier's Civilization IV", "Firaxis Games", 2005, "Step-by-step strategy"),
        ("Minecraft", "Mojang", 2009, "Sandbox"),
        ("The Witcher 3", "CD Project RED", 2014, "RPG")    
    '''
    cursor = conn.cursor()
    cursor.execute(fill_in)
    conn.commit()
    print('Table "games" was filled with data\n')


def view_table(conn):
    select_games = "SELECT * FROM games"
    cursor = conn.cursor()
    cursor.execute(select_games)
    result = cursor.fetchall()
    for row in result:
        print(row)


def drop_table(conn):
    drop_str = "DROP TABLE games"
    cursor = conn.cursor()
    cursor.execute(drop_str)
    print('Table "games" was dropped with data\n')


def explain_part(conn):
    explain_str = "EXPLAIN SELECT * FROM games WHERE release_year=2012"
    cursor = conn.cursor()
    cursor.execute(explain_str)
    result = cursor.fetchall()
    for row in result:
        print(row)


def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='games',
                                       user=input('Username: '),
                                       password=getpass('Password: '))
        if conn.is_connected():
            print('Connected to MySQL database')
            print(conn)
        create_db = 'CREATE DATABASE games'
        cursor = conn.cursor()
        cursor.execute(create_db)

        # show_db = 'SHOW DATABASES'
        # cursor.execute(show_db)
        #
        # for db in cursor:
        #     print(db)

    except Error as e:
        print(e)

    return conn
    # finally:
    #     conn.close()


if __name__ == '__main__':
    c = connect()
    # create_table(c)
    # fill_table(c)
    while True:
        ch = input('1 - to view the table\n2 - to drop the table\n'
                   '3 - to create the table\n4 - to check the partitions\n'
                   '0 - to exit\n')
        if ch == '0':
            break
        if ch == '1':
            view_table(c)
        if ch == '2':
            drop_table(c)
        if ch == '3':
            create_table(c)
        if ch == '4':
            explain_part(c)

    c.close()

