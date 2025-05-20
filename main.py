import sqlite3
from flask import Flask, render_template, request, url_for, redirect
from random import randint
from work_with_ticket import add_ticket_to_table, add_ticket_id_to_user, reduction_capacity

conection = sqlite3.connect('quidditch.bd',  check_same_thread=False)
cursor = conection.cursor()

app = Flask(__name__)

user_id = 0
admin_id = 0


#переносить на сторінку реєстрації
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('about'))


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('main.html')


@app.route('/about_log', methods=['GET', 'POST'])
def about_log():
    return render_template('main_log.html')



#сторрінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        log = request.form['name']
        passw = request.form['password']
        email_adress = request.form['email']
        log_correct = False
        user_info = []
        cursor.execute('SELECT * FROM users WHERE login = :us_login', {'us_login': log})
        if cursor.fetchall():
            log_correct = False
        else:
            log_correct = True

            cursor.execute('SELECT * FROM admins WHERE admin_log = :us_login', {'us_login': log})
            if cursor.fetchall():
                log_correct = False
            else:
                log_correct = True
            if log_correct:
                def rand_id(id=randint(100, 999)):
                    return id

                us_id_correct = True
                us_id = 0
                while (us_id_correct == True):
                    us_id = rand_id()
                    cursor.execute('SELECT * FROM users WHERE user_id = :id', {'id': us_id})
                    if cursor.fetchone():
                        us_id_correct = True
                    else:
                        us_id_correct = False
                    sqlite_insert_with_param = """INSERT INTO users
                                                        (user_id, login, password, email)
                                                        VALUES (?, ?, ?, ?);"""
                    user_info.append(us_id)
                    user_info.append(log)
                    user_info.append(passw)
                    user_info.append(email_adress)
                    cursor.execute(sqlite_insert_with_param, user_info)
                    conection.commit()
                    return redirect(url_for('login'))
        return redirect(url_for('register'))
    return render_template('register.html')


#сторінка логіну
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global admin_id
        global user_id
        admin_id = 0
        user_id = 0
        log = request.form['login']
        passw = request.form['password']
        login_exists_user = False
        login_exists_admin = False
        cursor.execute("SELECT * FROM users WHERE login = '" + log + "'")
        if cursor.fetchall():
            login_exists_user = True
        else:
            login_exists_user = False
        cursor.execute("SELECT * FROM admins WHERE admin_log = '" + log + "'")
        if cursor.fetchall():
            login_exists_admin = True
        else:
            login_exists_admin = False
        if login_exists_user == True and login_exists_admin == False:
            cursor.execute('SELECT * FROM users WHERE login = :log AND password = :passw',
                           {'log': log, 'passw': passw})
            if cursor.fetchall():
                user_id = [x[0] for x in
                           (cursor.execute('SELECT user_id FROM users WHERE login = :log AND password = :passw',
                                           {'log': log, 'passw': passw}).fetchall())]
                return redirect(url_for('user'))

        elif login_exists_user == False and login_exists_admin == True:
            cursor.execute('SELECT * FROM admins WHERE admin_log = :log AND admin_pass = :passw',
                           {'log': log, 'passw': passw})
            if cursor.fetchall():
                admin_id = [x[0] for x in (
                    cursor.execute('SELECT admin_id FROM admins WHERE admin_log = :log AND admin_pass = :passw',
                                   {'log': log, 'passw': passw}).fetchall())]
                return redirect(url_for('admin'))
        return redirect(url_for('login'))

    return render_template('login.html')


#форма додавання гри для адміна
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        game_info = []
        place = request.form['place']
        capacity = request.form['capacity']
        game_data = request.form['data']
        price = request.form['price']
        description = request.form['description']
        game_info.append(str(place))
        game_info.append(int(capacity))
        game_info.append(str(game_data))
        game_id_in_array = [x[0] for x in (cursor.execute('SELECT gameId FROM games').fetchall())]

        def check_game_id(game_id):
            flag = True
            for i in range(len(game_id_in_array)):
                if int(game_id_in_array[i]) == int(game_id):
                    flag = False
            return flag

        def create_game_id():
            game_id = randint(10, 99)
            return game_id

        game_id = create_game_id()
        check_flag = check_game_id(game_id)

        while check_flag != True:
            game_id = create_game_id()
            check_flag = check_game_id(game_id)
        game_info.append(int(game_id))

        game_info.append(str(admin_id[0]))
        game_info.append(price)
        game_info.append(description)

        sqlite_insert_with_param = """INSERT INTO games
                                            (place, capacity, data, gameId, admin_id, price, description)
                                            VALUES (?, ?, ?, ?, ?, ?, ?);"""
        cursor.execute(sqlite_insert_with_param, game_info)
        conection.commit()
        return redirect(url_for('admin_games'))
    return render_template('admin.html')


#відображення усіх ігор для адміна
@app.route('/admin_games', methods=['GET', 'POST'])
def admin_games():
    if request.method == 'POST':
        return redirect(url_for('admin_games'))

    list_with_rows = [x for x in (cursor.execute('SELECT * FROM games').fetchall())]
    return render_template('admin_games.html', rows=list_with_rows)


#видалення гри для адміна
@app.route('/delete/<row>', methods=['GET', 'POST'])
def del_game(row):
    #видалення айді з таблиці юзерів
    tikest_id_to_del = [x[0] for x in
                        (cursor.execute('SELECT ticket_id FROM tickets WHERE gameId = :id',
                                        {'id': int(row)}).fetchall())]

    info_users = [x for x in (
        cursor.execute('SELECT * FROM users').fetchall())]

    for i in range(len(info_users)):
        ids_in_list = list(info_users[i][4])
        ids_in_array_cor_user = []
        number = ''
        ids_in_list.append(' ')
        for f in range(len(ids_in_list)):
            if ids_in_list[f] != ' ':
                number = number + str(ids_in_list[f])
            else:
                if number != "":
                    ids_in_array_cor_user.append(int(number))
                    number = ''
                else:
                    pass

        ids_for_update_in_str = ""
        for j in range(len(ids_in_array_cor_user)):
            for e in range(len(tikest_id_to_del)):
                if int(ids_in_array_cor_user[j]) == int(tikest_id_to_del[e]):
                    pass
                else:
                    ids_for_update_in_str = f"{ids_for_update_in_str} {str(ids_in_array_cor_user[j])}"

        cursor.execute("""UPDATE users SET ticket_id = :tick_ids WHERE user_id = :id""",
                       {'tick_ids': ids_for_update_in_str, 'id': info_users[i][0]})
        conection.commit()


    #видалення квиткі
    cursor.execute('DELETE FROM tickets WHERE gameId = :id', {'id': int(row)})
    conection.commit()


    #видалення гри
    cursor.execute('DELETE FROM games WHERE gameId = :id', {'id': int(row)})
    conection.commit()

    return redirect(url_for('admin_games'))


#перша сторінка для юзера(з вибором гри та можливістю забронювати)
@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        pass
    us_id_cor = ""
    us_id = list(user_id)
    for i in range(len(us_id)):
        if us_id[i] == "[" or us_id[i] == "]" or us_id[i] == "'":
            pass
        else:
            us_id_cor = us_id_cor + us_id[i]
    name = [x[0] for x in (cursor.execute('SELECT login FROM users WHERE user_id = :id', {'id': str(us_id_cor)}).fetchall())]


    list_with_rows = [x for x in (cursor.execute('SELECT * FROM games').fetchall())]
    list_with_rows_cor = []
    for i in range(len(list_with_rows)):
        list_with_row = list(list_with_rows[i])
        list_with_rows_cor.append(list_with_row)


    return render_template('account.html', value=name[0], rows=list_with_rows_cor)


#сторінка з формою бронювання
@app.route('/user/<row>', methods=['GET', 'POST'])
def buy_ticket(row):
    if request.method == 'POST':
        # create ticket id
        def rand_id(id=randint(100, 999)):
            return id

        ticket_id_correct = True
        ticket_id = 0
        while (ticket_id_correct == True):
            ticket_id = rand_id()
            cursor.execute('SELECT * FROM tickets WHERE ticket_id = :id', {'id': str(row)})
            if cursor.fetchone():
                ticket_id_correct = True
            else:
                ticket_id_correct = False

        global user_id
        us_id_cor = ""
        us_id = list(user_id)
        for i in range(len(us_id)):
            if us_id[i] == "[" or us_id[i] == "]" or us_id[i] == "'":
                pass
            else:
                us_id_cor = us_id_cor + us_id[i]

        add_ticket_to_table(row, ticket_id)
        add_ticket_id_to_user(int(us_id_cor), int(ticket_id))
        reduction_capacity(row)
        return redirect(url_for('history'))

    #ім'я користувача
    us_id_cor = ""
    us_id = list(user_id)
    for i in range(len(us_id)):
        if us_id[i] == "[" or us_id[i] == "]" or us_id[i] == "'":
            pass
        else:
            us_id_cor = us_id_cor + us_id[i]
    name = [x[0] for x in
            (cursor.execute('SELECT login FROM users WHERE user_id = :id', {'id': str(us_id_cor)}).fetchall())]
    return render_template('buy_ticket.html', value=name[0])


#історія бронювань
@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        pass
    us_id_cor = ""
    us_id = list(user_id)
    for i in range(len(us_id)):
        if us_id[i] == "[" or us_id[i] == "]" or us_id[i] == "'":
            pass
        else:
            us_id_cor = us_id_cor + us_id[i]
    name = [x[0] for x in
            (cursor.execute('SELECT login FROM users WHERE user_id = :id', {'id': str(us_id_cor)}).fetchall())]

    #передача данних у фронт
    ticket_ids = [x[0] for x in (
        cursor.execute('SELECT ticket_id FROM users WHERE user_id = :id', {'id': str(us_id_cor)}).fetchall())]
    ticket_ids_list = list(ticket_ids[0])
    ticket_ids_in_array = []
    number = ''
    ticket_ids_list.append(' ')
    for i in range(len(ticket_ids_list)):
        if ticket_ids_list[i] != ' ':
            number = number + str(ticket_ids_list[i])
        else:
            if number != "":
                ticket_ids_in_array.append(int(number))
                number = ''
            else:
                pass

    array_with_all_info = []
    for i in range(len(ticket_ids_in_array)):
        info_for_ticket = []
        place = [x[0] for x in (cursor.execute('SELECT place FROM tickets WHERE ticket_id = :id',
                                               {'id': str(ticket_ids_in_array[i])}).fetchall())]
        place = str(place[0])

        data_ = [x[0] for x in (cursor.execute('SELECT data FROM tickets WHERE ticket_id = :id',
                                               {'id': str(ticket_ids_in_array[i])}).fetchall())]
        data_ = str(data_[0])

        t_id = [x[0] for x in (cursor.execute('SELECT ticket_id FROM tickets WHERE ticket_id = :id',
                                              {'id': str(ticket_ids_in_array[i])}).fetchall())]
        t_id = str(t_id[0])

        price = [x[0] for x in (cursor.execute('SELECT price FROM tickets WHERE ticket_id = :id',
                                               {'id': str(ticket_ids_in_array[i])}).fetchall())]
        price = price[0]

        gameId = [x[0] for x in (cursor.execute('SELECT gameId FROM tickets WHERE ticket_id = :id',
                                                {'id': str(ticket_ids_in_array[i])}).fetchall())]
        gameId = int(gameId[0])

        description = [x[0] for x in (cursor.execute('SELECT description FROM games WHERE gameId = :id',
                                                     {'id': int(gameId)}).fetchall())]
        description = str(description[0])

        info_for_ticket.append(place)
        info_for_ticket.append(data_)
        info_for_ticket.append(t_id)
        info_for_ticket.append(price)
        info_for_ticket.append(description)

        array_with_all_info.append(info_for_ticket)

    return render_template('user-history.html', value=name[0], rows=array_with_all_info)


port = 5100
if __name__ == '__main__':
    app.debug = True
    app.run()

cursor.close()