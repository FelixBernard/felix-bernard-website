from user.user import User

def set_up_user(request, response):
    if request.cookies.get("user") == "admin":
        tmp_user = User("admin")
        tmp_user.response = response
        return tmp_user
    else:
        tmp_user = User("client")
        tmp_user.response = response
        return tmp_user