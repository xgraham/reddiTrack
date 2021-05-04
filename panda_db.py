import sqlite3

import pandas as pd


# Read sqlite query results into a pandas DataFrame
def get_all_posts(time):
    sql = "SELECT Ticker, upvotes, comments," \
          "date(date, 'unixepoch', 'localtime') as 'y-m-d',title,postURL " \
          "from Posts "
    if RepresentsInt(time):
        print("adding time")
        sql += f" where date BETWEEN strftime('%s','now','-{str(time).rstrip()} hours') AND strftime('%s', 'now') order by date DESC;"
        print(sql)
    else:
        print("not adding time")
        sql += f" where date BETWEEN strftime('%s','now','-3 hours') AND strftime('%s', 'now') order by date DESC;"
        print(sql)
    return _get_db_query(sql)


def get_trending(time):
    sql = "SELECT Tickers.Ticker, SUM(upvotes), SUM(comments), count(*) as 'Number of Posts' from Posts left outer  join Tickers on Tickers.Ticker = Posts.Ticker "
    if RepresentsInt(time):
        print("adding time")
        sql += f" where date BETWEEN strftime('%s','now','-{str(time).rstrip()} hours') AND strftime('%s', 'now')"
        print(sql)
    else:
        print("not adding time")
        sql += f" where date BETWEEN strftime('%s','now','-3 hours') AND strftime('%s', 'now')"
        print(sql)

    sql += "group by Tickers.Ticker order by count(*) DESC;"
    return _get_db_query(sql)


def get_posts_by_ticker(ticker, time):
    sql = "Select datetime(date, 'unixepoch', 'localtime') as localtime, title, upvotes, comments, postURL from Posts " \
          f"where  Ticker = '{str(ticker).rstrip()}' and " \
          f"date BETWEEN strftime('%s','now','-{str(time).rstrip()} hours') AND strftime('%s', 'now') order by date DESC;"

    return _get_db_query(sql)


def _get_db_query(sql):
    con = sqlite3.connect("identifier.sqlite")
    df = pd.read_sql_query(sql, con)

    con.close()
    return df


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
