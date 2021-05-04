import csv
import re
import sched
import time
from multiprocessing.pool import ThreadPool as Pool

import praw

import db_driver

ticker_list_db = []
name_list_db = []


def check_reddit(_name_list_db, _ticker_list_db):
    reader = csv.reader(open("creds.csv") , delimiter=' ')
    data = list(reader)
    clientid = data[2]
    clientsecret = data[3]
    passsword = data[2]
    username = data[0]

    driver = db_driver.db_connector()
    if _name_list_db == []:
        _name_list_db = driver.get_common_names()
    if _ticker_list_db == []:
        _ticker_list_db = driver.get_tickers()

    reddit = praw.Reddit(client_id=clientid,
                         client_secret=clientsecret,
                         password=password,
                         user_agent='Reddit search data extractor by /u/' + username + '',
                         username=username)

    new_wsb = reddit.subreddit("wallstreetbets").new(limit=750)
    new_stocks = reddit.subreddit("stocks").new(limit=50)
    new_spacs = reddit.subreddit("spacs").new(limit=50)
    hot_list = reddit.subreddit("wallstreetbets+stocks").hot(limit=150)
    stockMarket_list = reddit.subreddit("stockmarket").new(limit=50)
    post_list = list(new_wsb) + list(new_stocks) + list(new_spacs) + list(hot_list) + list(stockMarket_list)

    pool_size = 10  # how many parallel calls to make, too high number may cause duplicates
    pool = Pool(pool_size)  # make a pool of workers with the previously set size

    for post in post_list:
        pool.apply_async(scrape_post, (post, _ticker_list_db, _name_list_db, driver,))

    pool.close()
    pool.join()


def scrape_post(post, _ticker_list_db, _name_list_db, driver):
    ticker_matches = [ticker for ticker in _ticker_list_db if
                      (research(ticker, post.title))]

    common_name_matches = [ticker for ticker in _name_list_db if
                           (re.search(f"[^a-zA-Z]{ticker}[^a-zA-Z]", " " + post.title + " ") is not None)]

    if ticker_matches.__len__() > 0:
        print("TICKER FOUND:" + str(ticker_matches))
        print(post.title, " | ", post.score)
        for item in ticker_matches:
            driver.insert_post(item, post.title, post.comments.list().__len__(), post.score,
                               post.created_utc, post.permalink, post.id)

    elif common_name_matches.__len__() > 0:
        print("COMMON NAME FOUND:" + str(common_name_matches))
        # print(post.title, " | ", post.score)
        for item in common_name_matches:
            driver.insert_common_name(item, post.title, post.comments.list().__len__(), post.score,
                                      post.created_utc, post.permalink, post.id)

    selftext = str(post.selftext)
    if selftext.__len__() > 0:
        ticker_matches = [ticker for ticker in _ticker_list_db if research(ticker, selftext)]

        for item in ticker_matches:
            print("Ticker Found in Self Text: " + item)
            driver.insert_post(item, post.title, post.comments.list().__len__(), post.score,
                               post.created_utc, post.permalink, post.id)
        common_name_matches = [ticker for ticker in _name_list_db if
                               (re.search(f"[^a-zA-Z]{ticker}[^a-zA-Z]", " " + selftext + " ") is not None)]

        for item in common_name_matches:
            print("Common Name Found in Self Text: " + item)
            driver.insert_common_name(item, post.title, post.comments.list().__len__(), post.score,
                                      post.created_utc, post.permalink, post.id)


def research(search_str, search_text):
    count = 0
    result = ""
    for char in search_str:
        if count == 0:
            result += char
            count = 1
        else:
            result += f"[{char.upper()}{char.lower()}]"
    return re.search(f"[^a-zA-Z]{result}[^a-zA-Z]", " " + search_text + " ") is not None


if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)
    check_reddit(name_list_db, ticker_list_db)


    def do_something(sc):
        print("Doing stuff...")
        check_reddit(name_list_db, ticker_list_db)
        s.enter(360, 1, do_something, (sc,))


    s.enter(600, 1, do_something, (s,))
    s.run()
