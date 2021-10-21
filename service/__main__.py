import http
import httpx
import logging

from flask import Flask, request
from service.config import emotion_url

from service.database.loader import save_wall, save_post
from service.database.queries import get_last_post_id

app = Flask(__name__)


@app.route("/api/v1/messages", methods=['POST'])
def process_message():
    data = request.json
    text = data['text']
    payload = {'text': text}
    emotion = httpx.post(emotion_url, json=payload)
    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)
    data['emotion'] = emotion.json()['emotions']
    save_wall(data)
    save_post(data)
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/api/v1/walls", methods=['GET'])
def process_wall():
    data = request.json
    wall_id = data['wall']
    last_post_id = get_last_post_id(wall_id)
    return last_post_id


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)
