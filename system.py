import sys
import os
import sql.init as init_files
import sql.sql as sql
from user.user import Admin
from scripts.func import hash_in

def count_clients():
    return 0

def init_server():
    # Alle DB's für Nutzer erzeugen
    # init_files.create_database('muj')
    init_files.create_general_user_table()
    init_files.create_general_client_table()
    init_files.create_general_client_session_id_table()
    init_files.create_general_member_table()
    init_files.create_general_member_session_id_table()
    init_files.create_general_admin_table()
    init_files.create_general_admin_session_id_table()
    init_files.create_general_admin_key_table()
    # Admin festlegen
    new_admin()

    # News Datenbank
    init_files.create_news_table()

    # System Datenbanken
    init_files.create_blocked_ip_table()
    init_files.create_log_table()
    init_files.create_errlog_table()
    init_files.create_requestlog_table()

def init_session():
    init_files.create_general_client_session_id_table()
    print('intit general user table')

def init():
    init_files.create_general_client_table()
    print('init gc')

def init_user():
    init_files.create_general_user_table()

def init_data_folder():
    try:
        os.makedirs('data/user/individual')
        os.makedirs('data/user/general')
        os.makedirs('data/shop')
    except:
        pass

def init_member():
    init_files.create_general_member_session_id_table()
    init_files.create_general_member_table()


def delete_output_log():
    os.remove('output.log')

def delete_all_dbs():
    import shutil

    if os.path.exists('data/user/general'):
        shutil.rmtree('data/user/general')
    if os.path.exists('data/user/individual'):
        shutil.rmtree('data/user/individual')

    os.mkdir('data/user/general')
    os.mkdir('data/user/individual')
    open('data/user/general/track.txt', 'a').close()
    open('data/user/individual/track.txt', 'a').close()

def all_session():
    while ((i := input('rank zum printen(quit zum beenden): ')) != 'quit'):
        sql.show_all(i)

def all():
    while ((i := input('rank zum printen(quit zum beenden): ')) != 'quit'):
        sql.show_all_gc(i)

def deletee():
    while ((i := input('rank zum deleten(quit zum beenden): ')) != 'quit'):
        while ((m := input('id zum deleten(quit zum beenden): ')) != 'quit'):
            sql.delete_user_session(i, m)

def deletee_2():
    while ((i := input('rank zum deleten(quit zum beenden): ')) != 'quit'):
        while ((m := input('id zum deleten(quit zum beenden): ')) != 'quit'):
            sql.delete_user(i, m)

def ss():
    cookie = input('cookie to search: ')
    print(sql.search_for_client_cookie(cookie))
    
def new_admin():
    e_mail = input('lege eine Admin email fest: ')
    password = input('lege ein Admin password fest: ')
    admin = Admin(email=e_mail)
    admin.set_new_admin(True)
    print('Das ist der Admin key (Als "key" cookie im Browser anlegen)', admin.key)
    sql.insert_general_user_table(admin.email, hash_in(f'{password}rr834fd'))
    sql.init_query(f"Update adminveri set active = 1 where id = '{admin.id}'")

def try_info():
    sql.tryyy_info()

def sql_query():
    while ((x:=input('Init/Insert/Delete -> 1 || Select -> 2 || quit_db -> abbruch: ')) != 'quit_db'):
        q = input('Geben sie ihre query ein: ')
        if int(x) == 1:
            try:
                print(sql.init_query_on_maindb(q))
            except:
                print('error')
        elif int(x) == 2:
            try:
                print(sql.universel_db_query_on_maindb(q))
            except:
                print('error')
        else:
            print('error')

def show_pic():
    files = os.listdir('static/pictures')
    for file in files:
        print(file)

def delete_pic():
    file = input('Welches Bild möchtest du löschen? ')
    try:
        os.remove(f'static/pictures/{file}')
        print(f'File {file} gelöscht')
    except:
        print('Es hat nicht geklappt')

def new_news():
    news = input("Was ist die neue News: ")
    id, err = sql.get_news('id')
    sql.insert_query(f"Insert into news values ({id+1}, '{news}')")

if __name__ == '__main__':
    dic = {
        'init server': init_server,
        'init user file/table': init,
        'init session': init_session,
        'init data folder(not needet)': init_data_folder,
        'init user': init_user,
        'init member': init_member,
        'clear(delete) output.log': delete_output_log,
        'all session': all_session,
        'delete': deletee,
        'delete2': deletee_2,
        'search': ss,
        'all': all,
        'new admin': new_admin,
        'delete dbs': delete_all_dbs,
        'try_info': try_info,
        'query': sql_query,
        'bilder anzeigen': show_pic,
        'bild loschen': delete_pic,
        'new news': new_news
    }
    while ((i := input('aktion(quit zum beenden): ')) != 'quit'):
        if i in dic:
            dic[i]()
        else:
            print('not in command list')
            print('--------------')
            for i in dic:
                print(i)