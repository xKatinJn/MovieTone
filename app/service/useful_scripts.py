from app import db
from app.models import PostChecked


def check_if_post_checked(current_user, post_id):
    checked_posts = PostChecked.query.filter_by(user_id=current_user.id, post_id=int(post_id)).first()
    if not checked_posts:
        checked_post = PostChecked(user_id=current_user.id, post_id=int(post_id))
        db.session.add(checked_post)
        db.session.commit()
