from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from transfer import Transfer

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route("/api/transfer", methods=['POST'])
def transfer_playlist():
    data = request.get_json()
    spotify_link = data.get('spotifyLink')
    if spotify_link:
        Transfer(spotify_link, socketio)
        return jsonify({"message": "Transfer Complete"})
    else:
        return jsonify({"error": "Spotify Link Error"}), 400

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)
