from flask_sqlalchemy import SQLAlchemy
"""
解决循环引用问题:这里只初始化SQLAlchemy，不与app进行绑定
"""
db = SQLAlchemy()