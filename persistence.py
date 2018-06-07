import sqlite3

conn = None


def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except Exception as exc:
        print(exc)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        raise e


def main():
    database = "database/my_db.sqlite"

    sql_create_evidences_table = """
        CREATE TABLE IF NOT EXISTS evidence (
        id integer PRIMARY KEY,
        file text NOT NULL,
        description text,
        name text,
        vulnerability text); """
    global conn
    conn = create_connection(database)
    if conn is None:
        print("Error! cannot create the database connection.")
        quit()
    else:
        create_table(conn, sql_create_evidences_table)
        conn.close()


if __name__ == '__main__':
    main()
