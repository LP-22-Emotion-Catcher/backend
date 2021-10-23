import http
import httpx
import logging

from flask import Flask, request
from service.config import emotion_url

from service.database.loader import save_wall, save_post, update_last_post_id
from service.database.queries import check_wall_exists, get_last_post_id

app = Flask(__name__)


@app.route("/api/v1/messages", methods=['POST'])
def process_message():
    data = request.json
    text = data['text']
    payload = {'text': text}
    emotion = httpx.post(emotion_url, json=payload)
    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)
    data['emotion'] = emotion.json()['emotions']
    save_post(data)
    if not check_wall_exists(data['wall']):
        save_wall(data)
    update_last_post_id(data['uid'])
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/api/v1/walls/<uid>", methods=['GET'])
def process_wall(uid):
    return get_last_post_id(uid)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)
