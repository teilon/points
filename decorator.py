import psycopg2
from config import db_config

def opendb(fn):

    def inner(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(db_config())
            return fn(conn, *args, **kwargs)
            conn.commit()
        except Exception as error:
            print(error)
            print("err")
        finally:
            if conn is not None:
                conn.close()
    return inner


def exec_to(conn, func, params):
    cur = conn.cursor()
    cur.callproc(func, params)
    cur.close()