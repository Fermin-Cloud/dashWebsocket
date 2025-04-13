"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# commands follow
"""

from dash import html, dcc

command_section = html.Section(
    [
        html.Form([
            html.Fieldset(
                [
                    html.Legend("Ejecución de Comandos"),
                    html.Label(
                        [
                            "Ingresa el comando:",
                            dcc.Input(
                                id="command-input",
                                type="text",
                                placeholder="Ej: ls -l /home",
                            )
                        ]
                    ),
                    html.Button("Ejecutar", id="execute-button", type="button"),
                ]
            )
        ])
        ,
        html.Pre(id="command-output"),
    ],
    className="command__container",
)

