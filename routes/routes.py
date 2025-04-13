import os
from flask import Flask, request
from flask_socketio import SocketIO
import socketio

server = Flask(__name__)

@server.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    """
    endpoint uploads files
    """
    filename = request.headers.get('X-Filename')
    chunk_index = int(request.headers.get('X-Chunk-Index', 0))
    total_chunks = int(request.headers.get('X-Total-Chunks', 1))

    if not filename:
        return 'Missing filename', 400

    file_path = os.path.join(server.config['UPLOAD_FOLDER'], filename)

    with open(file_path, 'ab') as f:
        f.write(request.data)

    progress = int((chunk_index + 1) / total_chunks * 100)
    socketio.emit('upload_progress', {'progress': progress})

    return 'Chunk received', 200
