# qa.py
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models import PostModel, LikeModel
from exts import db
from datetime import datetime

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    # 首页显示所有帖子
    posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    return render_template("shouye.html", posts=posts)


@bp.route("/chuanda")
def chuanda():
    category = request.args.get('category', '')
    if category:
        posts = PostModel.query.filter_by(category=category).order_by(PostModel.create_time.desc()).all()
    else:
        posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    return render_template("chuanda.html", posts=posts, current_category=category)


# qa.py
@bp.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')

        print("接收到的表单数据:", title)
        # 处理文件上传
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # 这里简化处理，实际项目中应该保存文件到服务器并生成URL
                filename = secure_filename(file.filename)
                file_path = os.path.join('static/uploads', filename)
                file.save(file_path)
                image_url = url_for('static', filename=f'uploads/{filename}')
            else:
                image_url = ''
        else:
            image_url = ''

        if not all([title, content, category]):
            flash('请填写完整信息', 'error')
            return redirect(url_for('qa.create_post'))

        post = PostModel(
            title=title,
            content=content,
            category=category,
            image_url=image_url,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()
        flash('帖子发布成功', 'success')
        return redirect(url_for('qa.chuanda'))

    return render_template("Published_content.html")


@bp.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = PostModel.query.get_or_404(post_id)

    # 检查是否已经点赞
    existing_like = LikeModel.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return {'status': 'unliked', 'likes_count': len(post.likes)}
    else:
        like = LikeModel(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return {'status': 'liked', 'likes_count': len(post.likes)}


# qa.py
@bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = PostModel.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        return jsonify({'success': False, 'message': '无权删除此帖子'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True, 'message': '帖子已删除'})