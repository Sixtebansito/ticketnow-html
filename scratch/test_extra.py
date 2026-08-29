import sqlite3

def check_db():
    conn = sqlite3.connect('instance/local_db.sqlite')
    c = conn.cursor()
    c.execute("PRAGMA table_info(Mercancia)")
    print(c.fetchall())
    
if __name__ == "__main__":
    check_db()
