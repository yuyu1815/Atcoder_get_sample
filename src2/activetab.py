from flask import Flask, request, jsonify
import json
import threading
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)  # これにより全てのオリジンからのリクエストを許可
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

shared_data = []
flask_thread = None  # Flaskスレッドの初期化

@app.route('/receive_data', methods=['POST'])
def receive_data():
    shared_data = request.json
    if shared_data is not None:
        with open("../qiita_write.json", mode="w", encoding="utf-8") as f:
            json.dump(shared_data, f)
        print(f"\rReceived data: {shared_data}", end="")
    return jsonify({'status': 'success'})

def run_flask():
    app.run(port=5000)

def start_flask():
    global flask_thread
    if flask_thread is None or not flask_thread.is_alive():
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.start()
    else:
        print("Flask server is already running.")

#if __name__ == '__main__':
#    start_flask()  # Flaskを起動
