# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import config
from exts import db
from models import UserModel
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = 'sb*^(shixuN/*8wcnm%#@^'
csrf = CSRFProtect(app)

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

db.init_app(app)
migrate = Migrate(app, db)

# 注册蓝图
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)