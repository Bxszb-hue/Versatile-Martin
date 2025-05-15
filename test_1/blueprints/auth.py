from flask import Blueprint
bp = Blueprint("auth",__name__,url_prefix="/auth")
#用户授权
#http://127.0.0.1:5000/auth/login
@bp.route("/login")
def login():
    return "登录成功"
