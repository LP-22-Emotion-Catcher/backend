from flask import Flask, jsonify, request
import http, logging


app = Flask(__name__)


@app.route("/api/v1/messages", methods = ['POST'])
def get_messages():
    data = request.json
    message = data['message']  
    logging.info(message)
    return '', http.HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)