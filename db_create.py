import sqlite3 as sq

with sq.connect("quidditch.bd") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS admins (
        admin_id TEXT PRIMARY KEY,
        admin_log TEXT, 
        admin_pass TEXT
        ) """)
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        login TEXT, 
        password TEXT,
        email TEXT,
        ticket_id TEXT,
        FOREIGN KEY(ticket_id) REFERENCES tickets(ticket_id)
        ) """)
    cur.execute("""CREATE TABLE IF NOT EXISTS tickets (
        place TEXT,
        data TEXT,
        ticket_id TEXT PRIMARY KEY,
        price FLOAT,
        gameId INTEGER,
        FOREIGN KEY(gameId) REFERENCES games(gameId)
        ) """)
    cur.execute("""CREATE TABLE IF NOT EXISTS games (
        place TEXT,
        capacity INTEGER,
        data TEXT,
        gameId INTEGER PRIMARY KEY,
        admin_id TEXT,
        price FLOAT,
        description TEXT,
        FOREIGN KEY(admin_id) REFERENCES admins(admin_id), 
        FOREIGN KEY(price) REFERENCES tickets(price),
        FOREIGN KEY(data) REFERENCES tickets(data) 
        ) """)

    #додавання адмінів(вручну)
    #sqlite_insert_with_param = """INSERT INTO admins
     #                    (admin_id, admin_log, admin_pass)
      #                  VALUES
       #                 ("777", "admin7", "pas123")"""
    #cur.execute(sqlite_insert_with_param)