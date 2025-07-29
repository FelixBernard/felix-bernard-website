import sql.sql as sql
from scripts.func import hash_in, create_key
import time
from datetime import datetime, timezone
import os

class User:
    def __init__(self, rank, request=None, response=None):
        self.hash = self.__hash__
        self.rank = rank
        self.request = request
        self.response = response
        self.cookie = None
        self.session = None
        self.ip = None
        self.entry_date = None

    def load(self):
        infos, err = sql.universel_db_query("Select * from user")

    def create_session(self, rank='C'):
        temp_time = str(time.time()) + str(os.urandom(16))
        hashed_text = hash_in(temp_time)
        hashed_text = rank + hashed_text + str(self.ip)
        return hashed_text

class Admin(User):
    def __init__(self, email=None, request=None, response=None):
        super().__init__("admin", request=request, response=response)
        self.id = None
        self.key = None
        self.email = email
        self.name = None
        self.second_name = None

    def load_new_admin(self, email):
        print("TODO")

    def load_admin(self, id=None, cookie=None):
        #TODO
        print("not implemented")

    def set_new_admin(self, email=None, password="random" ,first:bool=False):
        self.entry_date = datetime.now(timezone.utc)
        self.key = create_key()
        sql.insert_general_admin_table(self)
        self.id = sql.get_id("admin", self.email)

    def load_error_Admin(self):
        # Alle Attribute auf Error setzen
        self.id = -1
        self.key = "ERROR"
        self.email = "ERROR"
        self.name = "ERROR"
        self.second_name = "ERROR"

class Member(User):
    def __init__(self, request=None, response=None):
        super().__init__("member", request=request, response=response)
        self.id = None
        self.email = None
        self.name = None
        self.second_name = None

    def load_new_member(self):
        #TODO
        print("not implemented")

    def load_member(self, id=None, cookie=None):
        #TODO
        print("not implemented")
        
class Client(User):
    def __init__(self, request=None, response=None):
        super().__init__("client", request=request, response=response)
        self.id = None

    def load_new_client(self):
        self.session = hash_in(str(datetime.now(timezone.utc)))
        self.ip = self.request.access_route[0]
        sql.insert_general_client_session_id_table(client_session_id=self.session, ip=self.ip, time_stemp=datetime.now(timezone.utc), user_agent=self.request.headers.get("User-Agent"))

    def load_client(self, id=None, cookie=None):
        sql.get_client(id)