from app import create_app, db
from models import User

app = create_app('development')
app.app_context().push()


def create_database():
    """创建数据库和表"""
    db.create_all()
    print('数据库表已创建')

    # 创建管理员账户（开发环境）
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('管理员账户已创建，用户名: admin, 密码: admin123')


if __name__ == '__main__':
    create_database()