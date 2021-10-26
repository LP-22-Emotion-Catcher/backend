from service.database.db import db_session
from service.database.models import Wall, Post, Comment


def save_wall(data):
    walls = []
    wall = {'wall_id': data['wall'],
            'link': data['link'],
            'last_post_id': data['uid']
            }
    walls.append(wall)

    db_session.bulk_insert_mappings(Wall, walls, return_defaults=True)
    db_session.commit()
    return walls


def save_post(data):
    posts = []
    post = {'post_id': data['uid'],
            'link': data['link'],
            'author_id': data['author'],
            'text': data['text'],
            'likes': data['likes'],
            'reposts': data['reposts'],
            'comments': data['comments'],
            'views': data['views'],
            'emotion': data['emotion'],
            'created': data['created'],
            'wall_id': data['wall'],
            }
    posts.append(post)

    db_session.bulk_insert_mappings(Post, posts, return_defaults=True)
    db_session.commit()
    return posts


def update_last_post_id(wall_id, post_id):
    wall = Wall.query.filter_by(wall_id=wall_id).first()
    wall.last_post_id = post_id
    db_session.commit()
    return wall


def save_comment(data):
    comments = []
    comment = {
        'comment_id': data['uid'],
        'post_id': data['post_id'],
        'author_id': data['author_id'],
        'text': data['text'],
        'date_of_publishing': data['date_of_publishing'],
        'wall_id': data['wall_id'],
        }
    comments.append(comment)

    db_session.bulk_insert_mappings(Comment, comments, return_defaults=True)
    db_session.commit()
    return comments
