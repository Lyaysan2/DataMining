from matplotlib import pyplot as plt
from matplotlib import rcParams
import psycopg2.extras


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


# get 30 rows from db
page_rank = get_from_db("SELECT url, rank FROM page_rank order by rank desc limit 30")

index = []
values = []
for i in range(30):
    index.append(page_rank[i].get('url'))
    values.append(page_rank[i].get('rank'))

# create diagram for a page ranks
rcParams.update({'figure.autolayout': True})
plt.autoscale()
fig, ax = plt.subplots()
ax.bar(index, values)
ax.set_facecolor('white')
plt.xticks(rotation=90)
png_name = 'diagram.png'
plt.savefig(png_name, bbox_inches="tight")
