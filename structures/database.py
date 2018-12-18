import psycopg2

conn = psycopg2.connect(dbname='nbabrain2100', user='postgres')
conn.autocommit = True
cur = conn.cursor()

def query(q, vars=None):
    cur.execute(q, vars)
    for x in cur:
        yield x