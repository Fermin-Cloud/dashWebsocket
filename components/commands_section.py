"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# commands follow
"""

from dash import html, dcc

command_section = html.Section(
    [
        html.Fieldset(
            [
                html.Legend("Ejecución de Comandos"),
                html.Label("Ingresa el comando:", htmlFor="command-input"),
                dcc.Input(
                    id="command-input",
                    type="text",
                    placeholder="Ej: ls -l /home",
                    style={"width": "100%"}
                ),
                html.Button("Ejecutar", id="execute-button"),
                html.Div(
                    id="command-output",
                ),
            ]
        )
    ],
    className="command__container",
)
