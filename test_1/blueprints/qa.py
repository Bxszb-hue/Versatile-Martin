from flask import Blueprint
bp = Blueprint("qa",__name__,url_prefix="/")
#首页
#http://127.0.0.1:5000
@bp.route("/")
def index():
    return "首页"

@bp.route("/search")
def search():
    return "首页search"
@bp.route("/public_content")
def public_content():
    return "首页public_content"
