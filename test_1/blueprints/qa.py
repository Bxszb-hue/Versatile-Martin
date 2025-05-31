# qa.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
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

@bp.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')

        # 这里简化处理，实际项目中应该处理文件上传
        image_url = request.form.get('image_url', '')

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