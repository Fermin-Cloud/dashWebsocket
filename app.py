"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# init sv, templates and styles
"""

import os
import dash
from dash import html
from flask_socketio import SocketIO
import eventlet

# components
from components.uploader_section import upload_section
from components.commands_section import command_section

# routes
from routes.routes import server 

eventlet.monkey_patch()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


if __name__ == '__main__':
    socketio.run(server, debug=True)
