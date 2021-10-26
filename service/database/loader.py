from service.database.db import db_session
from service.database.models import Wall, Post


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
