import sql.sql as sql

class User:
    def __init__(self, rank):
        self.hash = self.__hash__
        self.rank = rank
        self.response = None
        self.cookie = None

    def load(self):
        infos, err = sql.universel_db_query("Select * from ")

class Admin(User):
    def __init__(self):
        super().__init__("admin")
        self.admin_id = None
        self.email = None
        self.name = None
        self.second_name = None

class Member(User):
    def __init__(self, rank):
        super().__init__("member")
        self.member_id = None
        self.email = None
        self.name = None
        self.second_name = None
        
class Client(User):
    def __init__(self):
        super().__init__("client")
        self.client_id = None