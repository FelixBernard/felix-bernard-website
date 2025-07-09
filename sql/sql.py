from sql.db_connector import *

def init_query(query):
    database =  mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=SQL_TOKEN,
        database="fw",
        auth_plugin='mysql_native_password',
        autocommit=False
    )
    try:
        curser = database.cursor()
        curser.execute(query)
        database.commit()
    finally:
        curser.close()
        database.close()

def init_query_on_maindb(query):
    return init_query(query)

def insert_query(query, db=None):
    init_query(query, db)

def universel_db_query(query, with_col_names:bool=True):
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=SQL_TOKEN,
        database="fw",
        auth_plugin='mysql_native_password',
        # autocommit=False
    )

    try:
        cursor = database.cursor()
        cursor.execute(query)
        
        # Spaltennamen abrufen
        column_names = [column[0] for column in cursor.description]
        
        results = []
        if with_col_names:
            results.append(dict(zip(column_names, column_names)))
        for row in cursor.fetchall():
            results.append(dict(zip(column_names, row)))

    except:
        results = [{"error": "error"}]
    
    finally:
        cursor.close()
        database.close()
        return results
    
def universel_db_query_on_maindb(query):
    return universel_db_query(query)

#print(universel_db_query("select * from functable;"))

def insert_general_user_table(email, password) -> bool:
    init_query(f"INSERT INTO user VALUES ('{email}', '{password}')")

def insert_general_client_table(client_id, ip_adress, time_stemp) -> bool:
    init_query(f"INSERT INTO client VALUES ('{client_id}', '{ip_adress}', '{time_stemp}')")

def insert_general_client_session_id_table(client_id, client_session_id, ip, time_stemp) -> bool:
    init_query(f"INSERT INTO clientsession VALUES ('{client_id}', '{client_session_id}', '{ip}', '{time_stemp}')")

def insert_general_member_table(member) -> bool:
    init_query(f"INSERT INTO member VALUES ('{member.id}', '{member.email}', '{member.ip_adress}', '{member.entry_date}', '{member.first_name}', '{member.last_name}', '{member.street}', '{member.house_number}', '{member.town}', '{member.town_number}', '{member.country}')")

def insert_general_member_session_id_table(member_id, member_session_id, ip, entry_date) -> bool:
    init_query(f"INSERT INTO membersession VALUES ('{member_id}', '{member_session_id}', '{ip}', '{entry_date}')")

def insert_general_admin_table(admin) -> bool:
    init_query(f"INSERT INTO admin VALUES ('{admin.id}', '{admin.email}', '{admin.ip_adress}', '{admin.entry_date}', '{admin.first_name}', '{admin.last_name}')")

def insert_general_admin_session_id_table(admin_id, admin_session_id, time_stemp) -> bool:
    init_query(f"INSERT INTO adminsession VALUES ('{admin_id}', '{admin_session_id}', '{time_stemp}')")

def insert_general_admin_key_table(admin_id, admin_key, active, time_stemp) -> bool:
    init_query(f"INSERT INTO adminveri VALUES ('{admin_id}', '{admin_key}', {active}, '{time_stemp}')")

def insert_sus_ip(ip, time, flag_count) -> None:
    print('sus ip')
    
def insert_blocked_ip(ip, time) -> None:
    init_query(f"INSERT INTO blockedip (ip, time_stemp) VALUES ('{ip}', '{time}')")

def insert_log(time, kind, status, mas):
    init_query(f"INSERT INTO log VALUES ('{time}', '{kind}', '{status}', '{mas}')")



def search_for_cookie(rank, cookie) -> int:
    # print_in_file('sql/search_for_cookie -- searche for cookie:' + str(cookie))
    foo =  universel_db_query(f"SELECT id FROM {rank}session WHERE session_id = '{cookie}'", False, True)
    # x = foo[0]["id"]
    # print(f"sql/search_for_cookie ---- rank: {rank}, foo[0][id]: {x}, err: {err}, cookie: {cookie}")
    return foo[0]["id"]

def search_for_client_cookie(cookie):
    return search_for_cookie('client', cookie)

def search_for_member_cookie(cookie):
    return search_for_cookie('member', cookie)

def search_for_admin_cookie(cookie):
    return search_for_cookie('admin', cookie)

def search_for_admin_key(key) -> int:
    foo= universel_db_query(f"SELECT id FROM adminveri WHERE veri = '{key}'", False, True)
    # print_in_file(f'sql/search for admin key -- i[0] = {foo}, err: {err}')
    return foo[0]["id"]
        
def search_for__existing_admin_key(key) -> int:
    foo = universel_db_query(f"SELECT veri FROM adminveri WHERE veri = '{key}'")
    # print_in_file(f'sql/search for admin key -- foo = {foo}')
    return foo

def search_for_user_email(email):
    foo = universel_db_query(f"SELECT * FROM user WHERE email = '{email}'", False, True)
    # print('sql.searchforuseremail -- ', foo)
    if len(foo) == 0:
        return 'err@mail', 'errhash'
    return foo[0]['email'], foo[0]['password']

def get_id(rank:str, email:str):
    foo = universel_db_query(f"SELECT id FROM {rank} WHERE email = '{email}'", False)
    print(f'sql/get_id -- foo = {foo}')
    if len(foo) == 0:
        return -1
    return foo[0]['id']

def get_password(email) -> str:
    return universel_db_query(f"SELECT password FROM user WHERE email = '{email}'")
        
def get_email(id) -> str:
    foo = universel_db_query(f"SELECT email FROM member WHERE id = '{id}'")
    return foo
        
def get_user(rank, cookie) -> int:
    foo = universel_db_query(f"SELECT id FROM {rank}session WHERE session_id = '{cookie}'")
    # print_in_file('sql/get_user -- searche for cookie:' + str(cookie) + 'foo => ' + foo)
    return foo

def get_client(id) -> list:
    foo = universel_db_query(f"SELECT * FROM client WHERE id = '{id}'")
    return foo[1]

def get_member(id) -> list:
    foo = universel_db_query(f"SELECT * FROM member WHERE id = '{id}'")
    return foo[1]

def get_member_new(id:int) -> list:
    # print(id)
    foo = universel_db_query(f"SELECT * FROM member WHERE id = '{id}'", False)
    print(foo)
    return foo[0]

def get_admin_key(id) -> int:
    foo = universel_db_query(f"SELECT veri FROM adminveri WHERE id = '{id}'", False)
    if len(foo) == 0:
        return -1
    else:
        return foo[0]['veri']
    
def get_admin_key_and_status(id) -> dict:
    foo = universel_db_query(f"SELECT veri, active FROM adminveri WHERE id = '{id}'", False)
    return foo


def show_all(rank) -> None:
    foo = universel_db_query(f"SELECT * FROM {rank}session")
    print('show_all -- ', foo)

def show_all_gc(rank) -> None:
    foo = universel_db_query(f"SELECT * FROM {rank}")
    print('show_all_gc -- ', foo)

def return_show_all(rank:str, limit:int, offset:int) -> list:
    # rank = rank.replace('_session', '')
    # rank = rank.replace('_key', '')
    foo = universel_db_query(f"SELECT * FROM {rank} LIMIT {limit} OFFSET {offset}")
    return foo
    
def delete_user_session(rank, session_id, key=None) -> None:
    insert_query(f"DELETE FROM {rank}session WHERE session_id = '{session_id}'")
    if rank == 'admin':
        insert_query(f"DELETE FROM adminveri WHERE veri = '{key}'")

def delete_user(rank, id) -> None:
    insert_query(f"DELETE FROM {rank} WHERE id = '{id}'")

def delete_password(email) -> None:
    # print('sql/delete_password-- delete email:', email)
    insert_query(f"DELETE FROM user WHERE email = '{email}'")


def get_news(colum):
    foo = universel_db_query('Select * from news', False)
    if len(foo) == 0:
        return 'Keine News'
    return foo[-1][colum]


def search_blocked_ip(ip):
    foo = universel_db_query(f"SELECT * from blockedip WHERE ip = '{ip}'", False)
    return foo
    

def tryyy_info() -> None:
    foo = universel_db_query(f"SELECT count(id), ip_adress FROM client group by ip_adress having count(id) > 1 order by ip_adress asc")
    for result in foo:
        print(result)

# from sqlalchemy import create_engine, Column, Integer, String, MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Verbindung zu MySQL-Datenbank herstellen
# DATABASE_URL = "mysql://root:passwd@localhost:3306/texst"
# engine = create_engine(DATABASE_URL)

# # Session konfigurieren
# Session = sessionmaker(bind=engine)
# session = Session()

# # Base-Klasse für ORM-Modelle erstellen
# Base = declarative_base()

# # Beispiel-ORM-Modell
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     email = Column(String(120))

# # Tabellen erstellen (falls sie noch nicht existieren)
# Base.metadata.create_all(engine)

# # Beispielabfrage
# def get_all_users():
#     return session.query(User).all()

# # Beispiel für das Einfügen von Daten
# def insert_user(name, email):
#     new_user = User(name=name, email=email)
#     session.add(new_user)
#     session.commit()

# insert_user("Max Mustermann", "max@example.com")

# # Beispiel für das Abfragen von Daten
# users = get_all_users()
# for user in users:
#     print(f"User: {user.name}, Email: {user.email}")

# # Einfügen eines neuen Nutzers
