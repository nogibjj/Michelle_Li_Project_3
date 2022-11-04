import csv
import sqlite3
from sqlite3 import Error

# create a database connection to a SQLite database
def create_connection(db_file):
    """create a database connection to a SQLite database
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
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn.cursor().execute(create_table_sql)
    except Error as e:
        print(e)


# add a data into table from CSV file
def add_data(conn):
    csv_file = r"friends_cleaned.csv"
    table_name = "friends"
    # specify encoding
    with open(csv_file, "r", encoding="utf-8") as f:
        records = csv.reader(f)
    cur = conn.cursor()
    next(records)  # skip header
    for r in records:
        sql = """ INSERT INTO """ + table_name + """(text, label) VALUES(?,?) """
        cur.execute(sql, r)


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

    # create a database connection
    c = create_connection("friends.db")

    # create friends table
    sql_create_friends_table = """ CREATE TABLE IF NOT EXISTS friends (
                                        text text NOT NULL,
                                        label text
                                    ); """
    # create friends table
    create_table(c, sql_create_friends_table)

    # insert data into friends table
    add_data(c)

    # query 1
    print("Query 1: find count of each label")
    rows = c.execute(query1).fetchall()

    # query 2
    print("Query 2: average length of text for each label")
    rows = c.execute(query2).fetchall()
    for row in rows:
        print(row)

    # query 3
    print("Query 3: find the longest text for each label")
    rows = c.execute(query3).fetchall()
    for row in rows:
        print(row)

    # query 4
    print("Query 4: find the shortest text for each label")
    rows = c.execute(query4).fetchall()
    for row in rows:
        print(row)

    # close connection
    c.close()
