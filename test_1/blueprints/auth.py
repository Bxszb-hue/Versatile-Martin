from datetime import datetime

from flask import url_for, Blueprint, render_template, request, jsonify, redirect, flash
from flask_mail import Message
from exts import db
from .forms import RegisterForm
from models import UserModel, PostModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint("auth", __name__, url_prefix="/auth")



@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # 获取表单数据
        email = request.form.get("login-username")
        password = request.form.get("login-password")

        user = UserModel.query.filter((UserModel.email == email) | (UserModel.username == email)).first()

        if not user:
            flash("用户名或邮箱不存在", "error")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, password):
            flash("密码错误", "error")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("登录成功", "success")
        return redirect(url_for("qa.index"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # 获取表单数据
        username = request.form.get('register-username')
        email = request.form.get('register-email')
        password = request.form.get('register-password')
        confirm_password = request.form.get('register-confirm-password')

        # 基本验证
        if not all([username, email, password, confirm_password]):
            flash("请填写所有字段", "error")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("两次密码不一致", "error")
            return redirect(url_for("auth.register"))

        # 检查用户名和邮箱是否已存在
        if UserModel.query.filter_by(username=username).first():
            flash("用户名已存在", "error")
            return redirect(url_for("auth.register"))

        if UserModel.query.filter_by(email=email).first():
            flash("邮箱已被注册", "error")
            return redirect(url_for("auth.register"))

        # 创建新用户
        try:
            user = UserModel(
                username=username,
                email=email,
                password=generate_password_hash(password),
                join_time=datetime.now()
            )
            db.session.add(user)
            db.session.commit()
            flash("注册成功，请登录", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash(f"注册失败: {str(e)}", "error")
            return redirect(url_for("auth.register"))

        return render_template("login.html")

@bp.route("/shouye")
def shouye():
    return render_template("shouye.html")

# auth.py
# auth.py
@bp.route("/personal_center")
@login_required
def personal_center():
    # 获取用户的帖子
    posts = PostModel.query.filter_by(user_id=current_user.id).order_by(PostModel.create_time.desc()).all()
    # 获取用户的帖子数量
    post_count = len(posts)
    return render_template("Personal Center.html", posts=posts, post_count=post_count)