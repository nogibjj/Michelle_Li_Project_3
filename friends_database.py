import csv
import sqlite3
from sqlite3 import Error

# create a database connection to a SQLite database
def create_connection(db_file):
    """ create a database connection to a SQLite database
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# create a table from the create_table_sql statement
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql) 
    except Error as e:
        print(e)

# add a data into table from CSV file
def add_data(conn, csv_file, table_name):
    file = open(csv_file)
    records = csv.reader(file)
    cur = conn.cursor()
    next(records) # skip header

    for row in records:
        sql = ''' INSERT INTO ''' + table_name + '''(text, label) VALUES(?,?) '''
        cur.execute(sql, row)

# Query 1: find count of each label
query1 = """SELECT label, COUNT(*) FROM friends GROUP BY label"""

# Query 2: average length of text for each label
query2 = """SELECT label, AVG(LENGTH(text)) FROM friends GROUP BY label"""

# Query 3: find the longest text for each label and print the text along with its label
query3 = """SELECT label, MAX(LENGTH(text)), text FROM friends GROUP BY label"""

# Query 4: find the shortest text for each label
query4 = """SELECT label, MIN(LENGTH(text)), text FROM friends GROUP BY label"""

# Query 2: find count of each label
if __name__ == "__main__":
    database = r"friends.db"
    csv_file = r"friends_cleaned.csv"
    table_name = "friends"

    # create a database connection
    conn = create_connection(database)

    # create friends table
    sql_create_friends_table = """ CREATE TABLE IF NOT EXISTS friends (
                                        text text NOT NULL,
                                        label text
                                    ); """
    # create friends table
    create_table(conn, sql_create_friends_table)

    # insert data into friends table
    add_data(conn, csv_file, table_name)

    # query 1
    print("Query 1: find count of each label")
    rows = conn.execute(query1).fetchall()
    for row in rows:
        print(row)
    
    # query 2
    print("Query 2: average length of text for each label")
    rows = conn.execute(query2).fetchall()
    for row in rows:
        print(row)

    # query 3
    print("Query 3: find the longest text for each label")
    rows = conn.execute(query3).fetchall()
    for row in rows:
        print(row)
    
    # query 4
    print("Query 4: find the shortest text for each label")
    rows = conn.execute(query4).fetchall()
    for row in rows:
        print(row)

    # close connection
    conn.close()
