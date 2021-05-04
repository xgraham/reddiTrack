import re
import sqlite3
from sqlite3 import Error

DB_DB = "identifier.sqlite"


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


def santize(str_):
    result = str(str_).replace('"', '').replace('\'', '')
    result = deEmojify(result)
    return result


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


class db_connector:
    db_file = DB_DB

    def __init__(self):
        self.conn = create_connection(self.db_file)

    def get_tickers(self):
        conn = self.conn

        sql = ''' SELECT Ticker,Name from TICKERS'''
        cur = conn.cursor()
        cur.execute(sql)
        list = cur.fetchall()
        new_list = [i[0] for i in list]
        return new_list

    def get_common_names(self):
        conn = self.conn
        sql = ''' SELECT Name,Ticker from Common_Names'''
        cur = conn.cursor()
        cur.execute(sql)
        append_list = cur.fetchall()
        new_append_list = [i[0] for i in append_list]
        return new_append_list

    def insert_post(self, ticker, title, comments, upvotes, postdate, url, postID):
        conn = create_connection(self.db_file)
        sql = f''' INSERT OR REPLACE INTO Posts(Ticker,title,comments,upvotes,date,postURL,redditID,postIDandticker)
        VALUES("{ticker}","{santize(title)}",{comments},{upvotes},"{postdate}","reddit.com{url}","{postID}","{ticker + postID}") '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()

        return cur.lastrowid

    def insert_common_name(self, common_name, title, comments, upvotes, date, url, postID):
        conn = create_connection(self.db_file)
        sql = f''' INSERT OR REPLACE INTO Posts(Ticker,title,comments,upvotes,date,postURL,redditID,postIDandticker)
                  VALUES((SELECT Ticker FROM Common_Names WHERE Name = '{common_name}'),"{santize(title)}",{comments},{upvotes},"{date}","reddit.com{url}","{postID}",(SELECT Ticker FROM Common_Names WHERE Name = '{common_name}')||"{postID}") '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        return cur.lastrowid


if __name__ == '__main__':
    driver = db_connector()
    ticker_list = driver.get_tickers()
    print(ticker_list)
