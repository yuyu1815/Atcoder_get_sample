from flask import Flask, request, jsonify
import threading,json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # これにより全てのオリジンからのリクエストを許可
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
shared_data = []
@app.route('/receive_data', methods=['POST'])
def receive_data():
    shared_data = request.json
    if shared_data is not None:
        with open("qiita_write.json", mode="w", encoding="utf-8") as f:
            json.dump(shared_data, f)
        print(f"\rReceived data:{ shared_data}",end="")
    return jsonify({'status': 'success'})

def run_flask():
    app.run(port=5000)


def start_flask():
    # Flaskを別スレッドで実行
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
def get_url_status():
    with open('qiita_write.json') as f:
        di = json.load(f)
    if di is not None:
        return di
    return None
# Flaskサーバーの開始
#start_flask()

# 他の処理やテスト実行
# get_url_status()
