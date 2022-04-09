import sys

import numpy as np
import psycopg2

np.set_printoptions(threshold=sys.maxsize)
import psycopg2.extras

dictionary_with_urls = []  # [{'url': '', 'refer': ''}, ...] - list of dictionary
links_dict = {}  # {'https://0': ['https://1', ...], ...} - for each parent a list with children
dict_code = {}  # {'https://www.apple.com/ru/': 0, ...} - code for each unique link
unique_links = []  # all unique links


def get_from_db(query):
    connection = psycopg2.connect(
        database='data_mining',
        user='postgres',
        password='qwerty007',
        port='5432',
    )
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    connection.autocommit = True
    cur.execute(query)
    temp_ans = cur.fetchall()
    ans = []
    for row in temp_ans:
        ans.append(dict(row))
    connection.commit()
    connection.close()
    return ans


def save_into_db(info):
    connection = psycopg2.connect(
        database='data_mining',
        user='postgres',
        password='qwerty007',
        port='5432',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    d = info
    keys = d.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert_query = 'INSERT INTO page_rank ({0}) VALUES ({1})'.format(columns, values)
    cursor.execute(cursor.mogrify(insert_query, d))
    connection.commit()
    connection.close()


def create_code():
    k = 0
    for i in unique_links:
        dict_code[i] = k
        k += 1


def create():
    c = 0
    while c < len(dictionary_with_urls):
        c = help_create(c)


def help_create(c):
    start = dictionary_with_urls[c].get('url')
    links_dict[dictionary_with_urls[c].get('url')] = []
    try:
        while dictionary_with_urls[c].get('url') == start:
            links_dict[dictionary_with_urls[c].get('url')].append(dictionary_with_urls[c].get('refer'))
            c += 1
    except IndexError:
        pass
    return c


def get_matrix(u_set):
    matrix = {}
    for columns in u_set:
        matrix[columns] = {}
        for rows in u_set:
            matrix[columns][rows] = 0.0
    return matrix


def fill_matrix(matrix):
    for url_from in links_dict.keys():
        for rows in links_dict[url_from]:
            url_index = dict_code.get(url_from)
            refer_index = dict_code.get(rows)
            matrix[url_index][refer_index] = 1.0
    return matrix


def probability(matrix):
    for i in range(len(matrix)):
        sum = np.sum(matrix[i])
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1.0:
                matrix[i][j] = 1.0 / sum
    return matrix


def create_matrix_form(mtx):
    temp = set().union(*mtx.values())
    res = [list(mtx.keys())]
    res += [[key] + [sub.get(key, 0) for sub in mtx.values()] for key in temp]

    res.pop(0)
    for i in range(len(res)):
        res[i].pop(0)

    return res


def get_unique_links():
    for item in dictionary_with_urls:
        if item['url'] not in unique_links:
            unique_links.append(item['url'])
        if item['refer'] not in unique_links:
            unique_links.append(item['refer'])


def vector_to_rank(list_of_ranks):
    for i in range(len(list_of_ranks)):
        for link, code in dict_code.items():
            if code == i:
                row = {"url": link,
                       "rank": list_of_ranks[i]
                       }
                save_into_db(row)


if __name__ == "__main__":
    # get all rows from db
    dictionary_with_urls = get_from_db("SELECT url, refer FROM url_info order by id")

    # create a links_dict (collapse keys)
    create()

    # get unique links
    get_unique_links()

    # for each unique link create a code to identify it
    create_code()

    # create matrix and set default 0
    mtx = get_matrix(dict_code.values())

    # set the value 1 if there is a path
    mtx = fill_matrix(mtx)

    mtx = create_matrix_form(mtx)
    mtx = np.array(mtx)

    # add probability to matrix
    mtx = probability(mtx)

    # print how many links we have
    print(len(unique_links))

    # raise the matrix to the power of its length
    final_matrix = np.linalg.matrix_power(mtx, len(unique_links))

    # create a vector of unique links length
    vector = [1 / len(unique_links)] * len(unique_links)
    vector = np.array(vector)

    # multiply vector by matrix
    rank_vector = vector.dot(final_matrix)

    # get a sum of ranks (should be 1)
    print(np.sum(rank_vector))

    # correlate a rank with correct link and save into a db
    vector_to_rank(rank_vector)

