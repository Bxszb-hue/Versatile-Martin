# create_db.py
from app import create_app, db
from models import UserModel, PostModel
from datetime import datetime

app = create_app('development')
app.app_context().push()


def create_database():
    """创建数据库和表"""
    db.create_all()
    print('数据库表已创建')

    # 创建管理员账户
    admin = UserModel.query.filter_by(username='admin').first()
    if not admin:
        admin = UserModel(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('管理员账户已创建，用户名: admin, 密码: admin123')

    # 添加测试帖子
    if PostModel.query.count() == 0:
        categories = ['休闲运动', '日常通勤', '休闲度假', '乐享派对']
        for i in range(1, 5):
            post = PostModel(
                title=f'测试帖子{i}',
                content=f'这是测试帖子{i}的内容',
                category=categories[i - 1],
                user_id=admin.id,
                image_url=f'https://picsum.photos/800/400?random={i}'
            )
            db.session.add(post)
        db.session.commit()
        print('测试帖子已添加')


if __name__ == '__main__':
    create_database()