from exts import db
from datetime import datetime
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # 邮箱注册、登录，必须要唯一
    join_time = db.Column(db.DateTime, default=datetime.now())

