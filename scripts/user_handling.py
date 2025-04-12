from user.user import User,Admin,Client

def set_up_user(request, response):
    if request.cookies.get("user") == "admin":
        tmp_user = Admin()
        tmp_user.response = response
        return tmp_user
    else:
        tmp_user = Client()
        tmp_user.response = response
        return tmp_user