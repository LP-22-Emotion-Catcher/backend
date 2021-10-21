from service.database.db import db_session
from service.database.models import Post


def get_last_post_id(wall_id):
    last_post_id = db_session.query(Post.uid).filter(Post.group == wall_id).order_by(Post.created.desc()).first()[0]
    if last_post_id:
        return str(last_post_id)
    else:
        return "No posts for this wall yet"
