import http
import httpx
import logging

from flask import Flask, request, jsonify, abort, make_response
from pydantic import ValidationError
from service.config import emotion_url

from service.database.loader import save_wall, save_post, update_last_post_id, save_comment
from service.database import queries

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/api/v1/messages", methods=['POST'])
def process_message():
    try:
        data = request.json
        logger.info('Just recieved a query for a wall config')
    except ValidationError as e:
        logger.info('Some problems with validation')
        abort(400, str(e))
    text = data['text']
    payload = {'text': text}

    try:
        emotion = httpx.post(f'{emotion_url}/api/v1/predict', json=payload)
    except httpx.ConnectError:
        logger.info('Can\'t connect with emotion service. No emotion color will be saved')
        data['emotion'] = None
        save_post(data)
        logger.info('New post has been saved without emotion color')
        update_last_post_id(wall_id=data['wall'], post_id=data['uid'])
        return '', http.HTTPStatus.CREATED

    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)
    data['emotion'] = emotion.json()['emotions']

    save_post(data)
    logger.info('New post has been saved with emotion color')
    update_last_post_id(wall_id=data['wall'], post_id=data['uid'])
    logger.info(f"Last post ID for this wall {data['wall']} was updated")
    return '', http.HTTPStatus.CREATED


@app.route('/api/v1/walls', methods=['POST'])
def add_wall():
    try:
        data = request.json
    except ValidationError as e:
        logger.info('Can\'t add a new wall')
        abort(400, str(e))

    save_wall(data)
    logger.info('wall has been created')
    return '', http.HTTPStatus.CREATED


@app.route("/api/v1/walls/<uid>", methods=['GET'])
def process_wall(uid):
    try:
        return queries.get_last_post_id(uid)
    except AttributeError:
        abort(make_response(jsonify(message=f"Wall with id {uid} doesn\'t exist."), 404))


@app.route("/api/v1/walls/", methods=['GET'])
def get_walls():
    walls = queries.get_walls()
    return jsonify(walls), http.HTTPStatus.OK


@app.route('/api/v1/walls/<uid>/posts/', methods=['GET'])
def get_posts(uid):
    emotion = request.args.get('emotion')
    posts = queries.get_posts(uid, emotion)
    return jsonify(posts), http.HTTPStatus.OK


@app.route("/api/v1/comments", methods=['POST'])
def process_comment():
    try:
        data = request.json
    except ValidationError as e:
        abort(400, str(e))

    save_comment(data)
    return '', http.HTTPStatus.CREATED


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000, debug=True)
