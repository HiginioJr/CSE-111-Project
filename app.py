import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable

def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn


def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def register(_conn):
    new_username = input("Enter new username: ")
    new_password = input("Enter new password: ")
    try:
        sql = f"""INSERT INTO user (u_username, u_password) VALUES('{new_username}', '{new_password}');"""
        _conn.execute(sql)
        _conn.commit()
    except Error as e:
        _conn.rollback()
        print(e)

def login(_conn, _username, _password):
    try:
        sql = f"""SELECT COUNT(u_username) FROM user where u_username = '{_username}' AND
        u_password = '{_password}';"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        return rows[0][0]

    except Error as e:
        _conn.rollback()
        print(e)

def update_username(_conn, _logged_in_username):
    new_username = input("Enter new username: ")
    try:
        sql = f"""UPDATE user SET u_username = '{new_username}' WHERE u_username = '{_logged_in_username}';"""
        _conn.execute(sql)
        _conn.commit()
        return new_username
    except Error as e:
        _conn.rollback()
        print(e)

def update_password(_conn, _logged_in_username):
    new_password = input("Enter new password: ")
    try:
        sql = f"""UPDATE user SET u_password = '{new_password}' WHERE u_username = '{_logged_in_username}';"""
        _conn.execute(sql)
        _conn.commit()
    except Error as e:
        _conn.rollback()
        print(e)

def insert_search(_conn, _bio_name, _park_name, _username):
    try:
        sql = f"""INSERT INTO search(se_bio_name, se_park) VALUES('{_bio_name}', '{_park_name}');"""
        _conn.execute(sql)
        _conn.commit()
        sql2 = f"""INSERT INTO user_searches 
        SELECT '{_username}', MAX(se_search_id) 
        FROM search;"""
        _conn.execute(sql2)
        _conn.commit()
    except Error as e:
        _conn.rollback()
        print(e)

def get_user_searches(_conn, _logged_in_username):
    try:
        sql = f"""SELECT se_bio_name, se_park FROM search, user_searches 
        WHERE us_username = '{_logged_in_username}' AND us_search_id = se_search_id;"""
        res = _conn.execute(sql)
        rows = res.fetchall()

        headers = ("animal/plant search term", "park")
        t = PrettyTable(headers)
        for row in rows:
            t.add_row(row)
        print(t)
        finish = input("Press any key to return")
    except Error as e:
        _conn.rollback()
        print(e)

def get_park_info(_conn, _park_name):
    try:
        sql = f"""SELECT p_park_code, p_park_name, p_acres, p_latitude, p_longitude
        FROM parks where p_park_name LIKE '%{_park_name}%';"""
        res = _conn.execute(sql)
        rows = res.fetchall()

        headers = ("park code", "park", "acres", "latitude", "longitude")
        t = PrettyTable(headers)
        for row in rows:
            t.add_row(row)
        print(t)
        return row[1]

    except Error as e:
        _conn.rollback()
        print(e)

def main():
    database = r"database.sqlite"

    conn = openConnection(database)
    login_status = False
    logged_in_username = ''
    print("---CALIFORNIA STATE PARK BIODIVERSITY DATABASE---")
    with conn:
        while True:
            user_input = input("Type \'L\' to login, type \'R\' to register a new account, or type \'Q\' to quit: ")
            if user_input == 'R':
                register(conn)
            elif user_input == 'L':
                username = input("Enter username: ")
                password = input("Enter password: ")
                login_result = login(conn, username, password)
                #username or password incorrect
                if login_result == 0:
                    print("Username or password incorrect")
                else:
                    logged_in_username = username
                    login_status = True
                    break
            elif user_input == 'Q':
                quit()
        
        while True:
            print("\n")
            print("Welcome, " + logged_in_username + ".")
            print("Select operation from list: ")
            print(" 'S': Search \n 'U': Update account \n 'V': View searches \n 'Q': Quit")
            command = input("Command: ")
            if command == 'Q':
                quit()
            #update account
            elif command == 'U':
                command = input("Enter 'U' to change username, or enter 'P' to change password: ")
                if command == 'U':
                    temp = update_username(conn, logged_in_username)
                    logged_in_username = temp
                elif command == 'P':
                    update_password(conn, logged_in_username)
            #view searches
            elif command == 'V':
                get_user_searches(conn, logged_in_username)
            #search
            elif command == 'S':
                print("Select search operation: ")
                print(" 'P': Search Parks \n 'S': Search Species")
                command = input("Command: ")
                #search parks
                if command == 'P':
                    search = input("Enter park name: ")
                    result = get_park_info(conn, search)
                    command = input("Would you like to save this search? Type 'Y' for yes, 'N' for no: ")
                    if command == 'Y':
                        insert_search(conn, 'none', result, logged_in_username)




    closeConnection(conn, database)


if __name__ == '__main__':
    main()