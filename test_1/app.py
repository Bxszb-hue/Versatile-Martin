import datetime
from flask import Flask,request,render_template
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
#pip install flask-migrate
import config
from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)
#创建一个sqlalchemy（app）一个数据库连接对象（sqlalchemy会自动读取app.config中的配置）

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

migrate = Migrate(app,db)
'''
@app.route('/')
def hello_world():
    return 'Hello World!'''

if __name__ == '__main__':
    app.run(debug=True)
