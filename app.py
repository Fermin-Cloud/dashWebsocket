"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# init sv, templates and styles
"""


import os
import subprocess
import dash
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch() # concurrencia

# components
from components.uploader_section import upload_section
from components.commands_section import command_section

# routes
from routes.routes import server 

# layouts and index
from layout import layout
from index import index_string


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

server.secret_key = b'resturant'
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(server, cors_allowed_origins="*")

app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)
app.index_string = index_string
app.layout = layout

# commands
@app.callback(
    dash.Output("command-output", "children"),
    dash.Input("execute-button", "n_clicks"),
    dash.State("command-input", "value"),
    prevent_initial_call=True
)
def run_command(n, command):
    if not command:
        return "No se ingresó un comando"

    def stream_output():
        proc = subprocess.Popen(
                    ['bash', '-c', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

        for line in proc.stdout:
            socketio.emit("command_output", {"data": line})
        proc.wait()
        socketio.emit("command_output", {"data": f"\nProceso terminado con código {proc.returncode}"})

    socketio.start_background_task(stream_output)

    return "Ejecutando comando... \n"

@socketio.on("connect")
def handle_connect():
    print("Cliente conectado")
    socketio.emit("command_output", {"data": "¡Conectado al WebSocket!\n"})

if __name__ == '__main__':
    socketio.run(server, debug=True)
