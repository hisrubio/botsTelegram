
import psycopg2

def conect():
    conn=None
    try:
        conn = psycopg2.connect(database="XXX", user = "xxx", password = "xxx", host = "xxx", port = "5432")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn="error"
    return conn

def statement(conn,query):
    print query
    cur = conn.cursor()
    try:
        cur.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print "falla"
        conn.roleback()
    return cur

def close(conn):
    if (conn != "error"):
        try:
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.roleback()
        finally:
            conn.commit()
    

    



