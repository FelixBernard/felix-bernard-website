from user.user import User,Admin,Client
from server_config import *

def set_up_user(request, response):
    if request.cookies.get(COOKIE_KEY) == COOKIE_VALUE:
        tmp_user = Admin()
        tmp_user.response = response
        return tmp_user
    else:
        tmp_user = Client()
        tmp_user.response = response
        return tmp_user