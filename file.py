import sqlite3 as sq

with sq.connect("quidditch.bd") as con:
    cur = con.cursor()
    sqlite_insert_with_param = """INSERT INTO admins
                        (admin_id, admin_log, admin_pass)
                          VALUES
                        ("777", "admin", "pas123")"""
    cur.execute(sqlite_insert_with_param)