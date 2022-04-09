from urllib.parse import urlparse, urljoin

import psycopg2
import psycopg2.extras
import requests
import validators
from bs4 import BeautifulSoup


def save_into_db(url_info):
    connection = psycopg2.connect(
        database='data_mining',
        user='postgres',
        password='qwerty007',
        port='5432',
    )
    connection.autocommit = True
    cursor = connection.cursor()
    d = url_info
    keys = d.keys()
    columns = ','.join(keys)
    values = ','.join(['%({})s'.format(k) for k in keys])
    insert_query = 'INSERT INTO url_info ({0}) VALUES ({1})'.format(columns, values)
    cursor.execute(cursor.mogrify(insert_query, d))
    connection.commit()
    connection.close()


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


# check the url
def valid_url(url):
    valid = validators.url(url)
    return valid


dict_db = {}  # dictionary for url and referer url


# browse the web page and extract all links.
def crawl(url):
    new_links = []

    try:
        # set timeout if link doesn't open
        soup = BeautifulSoup(requests.get(url, timeout=3).content, "html.parser")
        for a_tag in soup.findAll("a"):
            try:
                href = a_tag.attrs.get("href")
                if href == "" or href is None:
                    continue

                href = urljoin(url, href)
                parsed_href = urlparse(href)
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if href.endswith("/"):
                    href = href[:-1]
                if not valid_url(href):
                    continue

                # check for a loop and for repetition of records
                if (href != url) and (href not in new_links):
                    dict_db[url] = href
                    print(url, " : ", href)
                    new_links.append(href)

                    row = {"url": url,
                           "refer": href,
                           "depth": 1
                           }
                    save_into_db(row)

            except requests.Timeout as err:
                print(err)
    except requests.exceptions.RequestException as ex:
        print(ex)

    new_links2 = []
    dist_list = []
    for link in new_links:
        try:
            soup = BeautifulSoup(requests.get(link, timeout=3).content, "html.parser")
            for a_tag in soup.findAll("a"):
                try:
                    href = a_tag.attrs.get("href")
                    if href == "" or href is None:
                        continue

                    href = urljoin(link, href)
                    parsed_href = urlparse(href)
                    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

                    if href.endswith("/"):
                        href = href[:-1]
                    if not valid_url(href):
                        continue

                    if (href != link) and (href not in dist_list):
                        dict_db[link] = href
                        print(link, " : ", href)
                        new_links2.append(href)
                        dist_list.append(href)

                        row = {"url": link,
                               "refer": href,
                               "depth": 2
                               }
                        save_into_db(row)

                except requests.Timeout as err:
                    print(err)
        except requests.exceptions.RequestException as ex:
            print(ex)
        dist_list.clear()

    new_links3 = []
    for link in new_links2:
        if link not in dict_db.keys():
            try:
                soup = BeautifulSoup(requests.get(link, timeout=3).content, "html.parser")
                for a_tag in soup.findAll("a"):
                    try:
                        href = a_tag.attrs.get("href")
                        if href == "" or href is None:
                            continue

                        href = urljoin(link, href)
                        parsed_href = urlparse(href)
                        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

                        if href.endswith("/"):
                            href = href[:-1]
                        if not valid_url(href):
                            continue

                        if (href != link) and (href not in dist_list):
                            dict_db[link] = href
                            print(link, " : ", href)
                            new_links3.append(href)
                            dist_list.append(href)

                            row = {"url": link,
                                   "refer": href,
                                   "depth": 3
                                   }
                            save_into_db(row)

                    except requests.Timeout as err:
                        print(err)
            except requests.exceptions.RequestException as ex:
                print(ex)
            dist_list.clear()

    print("end of parsing")

    result = get_from_db("SELECT url, refer FROM url_info")
    links = []  # all links
    list_keys = []  # parent url
    dead_links = []  # dead links

    for i in result:
        if i['url'] not in links:
            links.append(i['url'])
        if i['url'] not in list_keys:
            list_keys.append(i['url'])
        if i['refer'] not in links:
            links.append(i['refer'])

    # get all dead links
    for dead in links:
        if dead not in list_keys:
            dead_links.append(dead)

    # find the parent url for dead link and save into db reverse relation
    for dead in dead_links:
        for i in result:
            if dead == i['refer']:
                row = {"url": i['refer'],
                       "refer": i['url'],
                       "depth": 3
                       }
                save_into_db(row)


if __name__ == "__main__":
    start_link = "https://goldapple.ru"
    crawl(start_link)
