import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable

def openConnection(_dbFile):
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)
    return conn


def closeConnection(_conn, _dbFile):
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

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

def insert_search(_conn, _bio_name, _park_name, _username, _search_type):
    try:
        sql = f"""INSERT INTO search(se_bio_name, se_park, se_search_type) VALUES('{_bio_name}', '{_park_name}', '{_search_type}');"""
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

def delete_search(_conn, _search_id):
    try:
        sql = f"""DELETE FROM search WHERE se_search_id = {_search_id};"""
        _conn.execute(sql)
        _conn.commit()
        sql2 = f"""DELETE FROM user_searches WHERE us_search_id = {_search_id};"""
        _conn.execute(sql2)
        _conn.commit()
    except Error as e:
        _conn.rollback()
        print(e)

def get_user_searches(_conn, _logged_in_username):
    try:
        sql = f"""SELECT se_bio_name, se_park, se_search_type, se_search_id FROM search, user_searches 
        WHERE us_username = '{_logged_in_username}' AND us_search_id = se_search_id;"""
        res = _conn.execute(sql)
        rows = res.fetchall()

        headers = ("animal/plant search term", "park", "search type", "search id")
        t = PrettyTable(headers)
        for row in rows:
            t.add_row(row)
        print(t)
        # finish = input("Press any key to return")
        return rows
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
        # print(rows[0])
        return rows[0][1]

    except Error as e:
        _conn.rollback()
        print(e)

def get_from_common_name(_conn, _search, _bio_type):
    #_bio_type is either 'A' for animal, or 'P' for plant
    try:
        sql = f"""SELECT cn_species_id from common_names WHERE cn_common_name LIKE "%{_search}%";"""
        res = _conn.execute(sql)
        rows = res.fetchall()

        headers = ("scientific name", "common name(s)", "park", "category", "order", "family")
        t = PrettyTable(headers)

        for row in rows:
            # print(row[0])
            if _bio_type == 'A':
                temp_sql = f"""SELECT a_scientific_name, cn_common_name, s_park_name, s_category, s_order, s_family
                FROM animals, species, common_names
                WHERE a_species_id = '{row[0]}'
                AND s_species_id = a_species_id
                AND cn_species_id = a_species_id;"""
                temp_res = _conn.execute(temp_sql)
                temp_rows = temp_res.fetchall()
                for temp_row in temp_rows:
                    t.add_row(temp_row)
            elif _bio_type == 'P':
                temp_sql = f"""SELECT pl_scientific_name, cn_common_name, s_park_name, s_category, s_order, s_family
                FROM plants, species, common_names
                WHERE pl_species_id = '{row[0]}'
                AND s_species_id = pl_species_id
                AND cn_species_id = pl_species_id;"""
                temp_res = _conn.execute(temp_sql)
                temp_rows = temp_res.fetchall()
                for temp_row in temp_rows:
                    t.add_row(temp_row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_from_animal_scientific(_conn, _sci_name):
    try:
        headers = ("scientific name", "common name(s)", "park", "category", "order", "family")
        t = PrettyTable(headers)

        sql = f"""SELECT a_scientific_name, cn_common_name, s_park_name, s_category, s_order, s_family
        FROM animals, species, common_names
        WHERE a_scientific_name LIKE '%{_sci_name}%'
        AND s_species_id = a_species_id
        AND cn_species_id = a_species_id
        GROUP BY s_park_name;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_from_plant_scientific(_conn, _sci_name):
    try:
        headers = ("scientific name", "common name(s)", "park", "category", "order", "family")
        t = PrettyTable(headers)

        sql = f"""SELECT pl_scientific_name, cn_common_name, s_park_name, s_category, s_order, s_family
        FROM plants, species, common_names
        WHERE pl_scientific_name LIKE '%{_sci_name}%'
        AND s_species_id = pl_species_id
        AND cn_species_id = pl_species_id
        GROUP BY s_park_name;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_park_num_species(_conn, _park):
    try:
        # headers = ("scientific name", "common name(s)", "park", "category", "order", "family")
        # t = PrettyTable(headers)

        sql = f"""SELECT COUNT(s_species_id)
        FROM parks, species, park_species
        WHERE p_park_name LIKE '%{_park}%'
        AND s_species_id = ps_species_id
        AND ps_park_code = p_park_code"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            # t.add_row(row)
            print("Number of species for " + _park + ": " + str(row[0]))
        # print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_park_counts(_conn, _park, _term):
    try:
        headers = (_term, "count")
        t = PrettyTable(headers)

        sql = f"""SELECT {_term}, COUNT({_term})
        FROM parks, species, park_species
        WHERE p_park_name LIKE '%{_park}%'
        AND s_species_id = ps_species_id
        AND ps_park_code = p_park_code
        GROUP BY {_term}"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_common_count(_conn, _common_name):
    try:
        sql = f"""SELECT COUNT(p_park_code)
        FROM parks, common_names, park_species
        WHERE cn_common_name LIKE '%{_common_name}%'
        AND cn_species_id = ps_species_id
        AND ps_park_code = p_park_code;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            # t.add_row(row)
            print("Found in " + str(row[0]) + " parks.")
        # print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_common_animal_conservation(_conn, _common_name):
    try:
        headers =("park", "park code", "state", "abundance", "conservation status")
        t = PrettyTable(headers)

        sql = f"""SELECT DISTINCT p_park_name, p_park_code, p_state, s_abundance, a_conservation_status
        FROM parks, common_names, park_species, animals, species
        WHERE cn_common_name LIKE '%{_common_name}%'
        AND cn_species_id = s_species_id
        AND a_species_id = s_species_id
        AND cn_species_id = ps_species_id
        AND ps_park_code = p_park_code;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_common_animal_misc(_conn, _common_name):
    try:
        headers =("scientific name", "occurrence", "nativeness", "seasonality", "record status")
        t = PrettyTable(headers)

        sql = f"""SELECT a_scientific_name, s_occurrence, s_nativeness, s_seasonality, a_record_status
        FROM common_names, animals, species
        WHERE cn_common_name LIKE '%{_common_name}%'
        AND cn_species_id = s_species_id
        AND a_species_id = s_species_id;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_common_plant_conservation(_conn, _common_name):
    try:
        headers =("park", "park code", "state", "abundance", "conservation status")
        t = PrettyTable(headers)

        sql = f"""SELECT DISTINCT p_park_name, p_park_code, p_state, s_abundance, pl_conservation_status
        FROM parks, common_names, park_species, plants, species
        WHERE cn_common_name LIKE '%{_common_name}%'
        AND cn_species_id = s_species_id
        AND pl_species_id = s_species_id
        AND cn_species_id = ps_species_id
        AND ps_park_code = p_park_code;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_common_plant_misc(_conn, _common_name):
    try:
        headers =("scientific name", "occurrence", "nativeness", "seasonality", "record status")
        t = PrettyTable(headers)

        sql = f"""SELECT pl_scientific_name, s_occurrence, s_nativeness, s_seasonality, pl_record_status
        FROM common_names, plants, species
        WHERE cn_common_name LIKE '%{_common_name}%'
        AND cn_species_id = s_species_id
        AND pl_species_id = s_species_id;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_scientific_count(_conn, _sci_name, _bio_type):
    try:
        if _bio_type == 'A':
            sql = f"""SELECT COUNT(p_park_code)
            FROM parks, animals, park_species
            WHERE a_scientific_name LIKE '%{_sci_name}%'
            AND a_species_id = ps_species_id
            AND ps_park_code = p_park_code;"""
            res = _conn.execute(sql)
            rows = res.fetchall()
            # print(rows)
            for row in rows:
                # t.add_row(row)
                print("Found in " + str(row[0]) + " parks.")
        elif _bio_type == 'P':
            sql = f"""SELECT COUNT(p_park_code)
            FROM parks, plants, park_species
            WHERE pl_scientific_name LIKE '%{_sci_name}%'
            AND pl_species_id = ps_species_id
            AND ps_park_code = p_park_code;"""
            res = _conn.execute(sql)
            rows = res.fetchall()
            # print(rows)
            for row in rows:
                # t.add_row(row)
                print("Found in " + str(row[0]) + " parks.")
    except Error as e:
        _conn.rollback()
        print(e)

def get_scientific_animal_conservation(_conn, _sci_name):
    try:
        headers =("park", "park code", "state", "abundance", "conservation status")
        t = PrettyTable(headers)

        sql = f"""SELECT DISTINCT p_park_name, p_park_code, p_state, s_abundance, a_conservation_status
        FROM parks, park_species, animals, species
        WHERE a_scientific_name LIKE '%{_sci_name}%'
        AND a_species_id = s_species_id
        AND ps_park_code = p_park_code;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_scientific_animal_misc(_conn, _sci_name):
    try:
        headers =("scientific name", "occurrence", "nativeness", "seasonality", "record status")
        t = PrettyTable(headers)

        sql = f"""SELECT a_scientific_name, s_occurrence, s_nativeness, s_seasonality, a_record_status
        FROM animals, species
        WHERE a_scientific_name LIKE '%{_sci_name}%'
        AND a_species_id = s_species_id;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_scientific_plant_conservation(_conn, _sci_name):
    try:
        headers =("park", "park code", "state", "abundance", "conservation status")
        t = PrettyTable(headers)

        sql = f"""SELECT DISTINCT p_park_name, p_park_code, p_state, s_abundance, pl_conservation_status
        FROM parks, park_species, plants, species
        WHERE pl_scientific_name LIKE '%{_sci_name}%'
        AND pl_species_id = s_species_id
        AND ps_park_code = p_park_code;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
    except Error as e:
        _conn.rollback()
        print(e)

def get_scientific_plant_misc(_conn, _sci_name):
    try:
        headers =("scientific name", "occurrence", "nativeness", "seasonality", "record status")
        t = PrettyTable(headers)

        sql = f"""SELECT pl_scientific_name, s_occurrence, s_nativeness, s_seasonality, pl_record_status
        FROM plants, species
        WHERE pl_scientific_name LIKE '%{_sci_name}%'
        AND pl_species_id = s_species_id;"""
        res = _conn.execute(sql)
        rows = res.fetchall()
        # print(rows)
        for row in rows:
            t.add_row(row)
            # print(row)
        print(t)
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
            command = ''
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
                result = get_user_searches(conn, logged_in_username)
                # command = input("Type 'S' to search from saved searches, 'D' to delete a search, of 'Q' to return: ")
                command = input("To select a search, enter the search id or type 'Q' to return: ")
                for row in result:
                    #search is a park
                    if str(row[3]) == command and row[2] == 'park':
                        print("Enter commands from list: ")
                        print(" 'S': Search again \n 'N': Get number of species \n 'C': Get category count \n 'O': Get order count \n 'F': Get family count \n 'D': Delete search \n 'Q': Return")
                        command = input("Command: ")
                        if command == 'S':
                            res = get_park_info(conn, row[1])
                            finish = input("Press any key to return")
                        elif command == 'N':
                            get_park_num_species(conn, row[1])
                            finish = input("Press any key to return")
                        elif command == 'C':
                            get_park_counts(conn, row[1], "s_category")
                            finish = input("Press any key to return")
                        elif command == 'O':
                            get_park_counts(conn, row[1], "s_order")
                            finish = input("Press any key to return")
                        elif command == 'F':
                            get_park_counts(conn, row[1], "s_family")
                            finish = input("Press any key to return")
                        elif command == 'D':
                            delete_search(conn, row[3])
                            finish = input("Press any key to return")
                        else:
                            continue
                    #search is common animal
                    elif str(row[3]) == command and row[2] == 'common A':
                        print("Enter commands from list: ")
                        print(" 'S': Search again \n 'N': Get number of parks it is found in \n 'C': Get conservation stats \n 'M': Miscellaneous info \n 'D': Delete search \n 'Q': Return")
                        command = input("Command: ")
                        if command == 'S':
                            get_from_common_name(conn, row[0], 'A')
                            finish = input("Press any key to return")
                        elif command == 'N':
                            get_common_count(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'C':
                            get_common_animal_conservation(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'M':
                            get_common_animal_misc(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'D':
                            delete_search(conn, row[3])
                            finish = input("Press any key to return")
                        else:
                            continue
                    #search is common plant
                    elif str(row[3]) == command and row[2] == 'common P':
                        print("Enter commands from list: ")
                        print(" 'S': Search again \n 'N': Get number of parks it is found in \n 'C': Get conservation stats \n 'M': Miscellaneous info \n 'D': Delete search \n 'Q': Return")
                        command = input("Command: ")
                        if command == 'S':
                            get_from_common_name(conn, row[0], 'P')
                            finish = input("Press any key to return")
                        elif command == 'N':
                            get_common_count(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'C':
                            get_common_plant_conservation(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'M':
                            get_common_plant_misc(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'D':
                            delete_search(conn, row[3])
                            finish = input("Press any key to return")
                        else:
                            continue
                    #search is scientific animal
                    elif str(row[3]) == command and row[2] == 'sci animal':
                        print("Enter commands from list: ")
                        print(" 'S': Search again \n 'N': Get number of parks it is found in \n 'C': Get conservation stats \n 'M': Miscellaneous info \n 'D': Delete search \n 'Q': Return")
                        command = input("Command: ")
                        if command == 'S':
                            get_from_animal_scientific(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'N':
                            get_scientific_count(conn, row[0], 'A')
                            finish = input("Press any key to return")
                        elif command == 'C':
                            get_scientific_animal_conservation(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'M':
                            get_scientific_animal_misc(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'D':
                            delete_search(conn, row[3])
                            finish = input("Press any key to return")
                        else:
                            continue
                    #search is scientific plant
                    elif str(row[3]) == command and row[2] == 'sci plant':
                        print("Enter commands from list: ")
                        print(" 'S': Search again \n 'N': Get number of parks it is found in \n 'C': Get conservation stats \n 'M': Miscellaneous info \n 'D': Delete search \n 'Q': Return")
                        command = input("Command: ")
                        if command == 'S':
                            get_from_plant_scientific(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'N':
                            get_scientific_count(conn, row[0], 'P')
                            finish = input("Press any key to return")
                        elif command == 'C':
                            get_scientific_plant_conservation(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'M':
                            get_scientific_plant_misc(conn, row[0])
                            finish = input("Press any key to return")
                        elif command == 'D':
                            delete_search(conn, row[3])
                            finish = input("Press any key to return")
                        else:
                            continue
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
                        insert_search(conn, 'none', result, logged_in_username, 'park')
                #search species
                elif command == 'S':
                    print("Select search options:")
                    print(" 'C': Search common name \n 'A': Search animal by scientific name \n 'P': Search plant by scientific name \n 'Q': Return")
                    command = input("Command: ")
                    #search common name
                    if command == 'C':
                        command = input("Plant 'P' or Animal 'A'?: ")
                        if command != 'P' and command != 'A':
                            command = input("Invalid input. Press any key to continue.")
                            continue
                        search = input("Enter common name: ")
                        get_from_common_name(conn, search, command)
                        temp = command
                        command = input("Would you like to save this search? Type 'Y' for yes, 'N' for no: ")
                        if command == 'Y':
                            insert_search(conn, search, 'n/a', logged_in_username, 'common ' + temp)
                    #search animal by scientifc name
                    elif command == 'A':
                        search = input("Enter scientific name for animal: ")
                        get_from_animal_scientific(conn, search)
                        command = input("Would you like to save this search? Type 'Y' for yes, 'N' for no: ")
                        if command == 'Y':
                            insert_search(conn, search, 'n/a', logged_in_username, 'sci animal')
                    elif command == 'P':
                        search = input("Enter scientific name for plant: ")
                        get_from_plant_scientific(conn, search)
                        command = input("Would you like to save this search? Type 'Y' for yes, 'N' for no: ")
                        if command == 'Y':
                            insert_search(conn, search, 'n/a', logged_in_username, 'sci plant')
                       




    closeConnection(conn, database)


if __name__ == '__main__':
    main()