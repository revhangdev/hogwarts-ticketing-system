import sqlite3

conection = sqlite3.connect('quidditch.bd', check_same_thread=False)
cursor = conection.cursor()


# додаємо квиток в таблицю
def add_ticket_to_table(gameId, ticket_id):
    ticket_info = []
    place = [x[0] for x in
             (cursor.execute('SELECT place FROM games WHERE gameId = :id', {'id': str(gameId)}).fetchall())]
    data = [x[0] for x in (cursor.execute('SELECT data FROM games WHERE gameId = :id', {'id': str(gameId)}).fetchall())]

    price = [x[0] for x in
             (cursor.execute('SELECT price FROM games WHERE gameId = :id', {'id': str(gameId)}).fetchall())]
    game_id = int(gameId)
    ticket_info.append(str(place[0]))
    ticket_info.append(str(data[0]))
    ticket_info.append(str(ticket_id))
    ticket_info.append(price[0])
    ticket_info.append(int(game_id))
    sqlite_insert_with_param = """INSERT INTO tickets
                                            (place, data, ticket_id, price, gameId)
                                            VALUES (?, ?, ?, ?, ?);"""
    cursor.execute(sqlite_insert_with_param, ticket_info)
    conection.commit()


# додаємо тікет айді до таблиці користувачів
def add_ticket_id_to_user(us_id, ticket_id):
     old_ticket_id = [x[0] for x in
             (cursor.execute('SELECT ticket_id FROM users WHERE user_id = :id', {'id': str(us_id)}).fetchall())]
     old_ticket_id = old_ticket_id[0]
     if old_ticket_id == None:
         new_ticket_ids = ticket_id

         cursor.execute("""UPDATE users SET ticket_id = :tick_ids WHERE user_id = :id""",
                        {'tick_ids': new_ticket_ids, 'id': us_id})
         conection.commit()
     else:
         new_ticket_ids = f"{old_ticket_id} {ticket_id}"

         cursor.execute("""UPDATE users SET ticket_id = :tick_ids WHERE user_id = :id""", {'tick_ids': new_ticket_ids, 'id': us_id})

         conection.commit()


#зменшення капасіті в таблиці ігор
def reduction_capacity(game_id):
    place_game_table = [x[0] for x in
                        (cursor.execute('SELECT place FROM games WHERE gameId = :id', {'id': str(game_id)}).fetchall())]
    capacity_old_game_table = [x[0] for x in
                               (cursor.execute('SELECT capacity FROM games WHERE gameId = :id',
                                               {'id': str(game_id)}).fetchall())]
    data_game_table = [x[0] for x in
                       (cursor.execute('SELECT data FROM games WHERE gameId = :id', {'id': str(game_id)}).fetchall())]
    game_id_game_table = int(game_id)
    admin_id_game_table = [x[0] for x in
                           (cursor.execute('SELECT admin_id FROM games WHERE gameId = :id',
                                           {'id': str(game_id)}).fetchall())]
    price_game_table = [x[0] for x in
                        (cursor.execute('SELECT price FROM games WHERE gameId = :id', {'id': str(game_id)}).fetchall())]
    description_game_table = [x[0] for x in
                              (cursor.execute('SELECT description FROM games WHERE gameId = :id',
                                              {'id': str(game_id)}).fetchall())]
    capacity_new_game_table = int(int(capacity_old_game_table[0]) - 1)

    game_info_for_append = []
    game_info_for_append.append(str(place_game_table[0]))
    game_info_for_append.append(int(capacity_new_game_table))
    game_info_for_append.append(str(data_game_table[0]))
    game_info_for_append.append(int(game_id_game_table))
    game_info_for_append.append(str(admin_id_game_table[0]))
    game_info_for_append.append(price_game_table[0])
    game_info_for_append.append(str(description_game_table[0]))

    cursor.execute("DELETE FROM games WHERE gameId = :id", {'id': str(game_id)})
    conection.commit()

    sqlite_insert_with_param = """INSERT INTO games
                                        (place, capacity, data, gameId, admin_id, price, description)
                                        VALUES (?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(sqlite_insert_with_param, game_info_for_append)
    conection.commit()