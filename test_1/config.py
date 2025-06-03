"""
项目配置
"""
#mysql所在主机ip
HOSTNAME = '127.0.0.1'
#mysql监听的端口号，默认3306
PORT = 3306
#连接mysql的用户名（自己的）
USERNAME = 'root'
#连接mysql的密码（自己的）
PASSWORD = '123456'
#mysql上的数据库名称(需要先创建完成)
DATABASE = 'webshixun'
#app.config中配置flask连接数据库配置
#'mysql+[driver]://[USERNAME]:[PASSWORD]@[HOSTNAME]:[PORT]/[DATABASE]?charset=utf-8'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

# 上传文件配置
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}