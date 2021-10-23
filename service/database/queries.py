from service.database.db import db_session
from service.database.models import Post, Wall


def get_last_post_id(wall_id):
    last_post_id = db_session.query(Wall.last_post_id).filter(Wall.name == wall_id).first()
    if last_post_id:
        return str(last_post_id)
    else:
        return None


# Old way, currently not using
def get_last_post_id2(wall_id):
    last_post_id = db_session.query(Post.uid).filter(Post.group == wall_id).order_by(Post.created.desc()).first()[0]
    if last_post_id:
        return str(last_post_id)
    else:
        return None


def check_wall_exists(wall_id):
    wall_exists = db_session.query(Wall.name).filter(Wall.name == int(wall_id))
    if wall_exists:
        return True
    return False
