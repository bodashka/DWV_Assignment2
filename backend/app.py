from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import queue

app = Flask(__name__)
CORS(app)

event_queue = queue.Queue()

@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.get_json()
    event_queue.put(data)
    return jsonify({'status': 'received'}), 200

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            data = event_queue.get()
            yield f"data: {json.dumps(data)}\n\n"
    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
