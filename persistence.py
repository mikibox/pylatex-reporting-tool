import sqlite3

sqlite_file = "database/my_db.sqlite"
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute(
    '''
    CREATE TABLE IF NOT EXISTS evidence (
    id integer PRIMARY KEY,
    file text NOT NULL,
    description text,
    name text,
    vulnerability text);
     '''
)

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

conn.close()
