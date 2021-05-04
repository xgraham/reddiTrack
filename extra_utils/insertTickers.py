import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create

     database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT OR REPLACE INTO Tickers(Ticker,Name)
              VALUES(?,?) '''
    cur = conn.cursor()
    ticker_list = cur.execute(sql, project).fetchall()
    conn.commit()
    return ticker_list


if __name__ == '__main__':
    conn = create_connection(r"/identifier.sqlite")
    f = open("../CleanList.csv", "r")
    spac_list = f.readlines()
    count = 0
    for item in spac_list:
        item = item.rstrip()
        items = item.split(",")
        count +=1
        print(count, items[1],items[2])
        project = (items[1],items[2])
        create_project(conn,project)