"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# init sv, templates and styles
"""

import os
from dash import html
from flask import Flask, request
from flask_socketio import SocketIO
import dash
import eventlet

# components
from components.uploader_section import upload_section
from components.commands_section import command_section

eventlet.monkey_patch()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(server, cors_allowed_origins="*")

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

#  Socket.IO en el HTML
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
        <link rel="stylesheet" href="./static/styles.css">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Main([
    upload_section,
    command_section,
    html.Script(src="/static/upload-handler.js")
], className="main__container")

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

if __name__ == '__main__':
    socketio.run(server, debug=True)
