import re
import sqlite3


def _get_db_query(sql):
    con = sqlite3.connect("../identifier.sqlite")
    cur = con.cursor()
    cur.execute(sql)
    list = cur.fetchall()
    con.close()
    return list


def convertTuple(tup):
    str = ''.join(tup)
    char_list = [str[j] for j in range(len(str)) if ord(str[j]) in range(65536)]
    result = ''
    for j in char_list:
        result = result + j
    return santize(result)


def santize(str_):
    result = str(str_).replace('"', '').replace('\'', '')
    return remove_emoji(result)


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


if __name__ == "__main__":

    sql = "SELECT postID, title from Posts"
    list = _get_db_query(sql)
    con = sqlite3.connect("../identifier.sqlite")

    new_list = []
    for item in list:
        _str = convertTuple(item[1])

        print("cleaned:", item[0], _str)
        sql = f"UPDATE Posts set title = '{_str}' where PostID = '{item[0]}'"

        cur = con.cursor()
        cur.execute(sql)
        con.commit()

    con.close()
