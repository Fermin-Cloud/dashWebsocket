"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# upload and websocket component
"""

from dash import html, dcc

message: str = 'Arrastra y suelta o haz clic para seleccionar'
title: str = 'Subida de Archivos con progreso: Drag & drop'

upload_section = html.Section(
    [
        html.Form(
            [
                html.Fieldset(
                    [
                        html.Legend(f"{title}"),
                        html.Label(
                            [
                                dcc.Upload(
                                    id='upload-data',
                                    multiple=False,
                                ),
                                html.Div(
                                    [
                                        html.Strong(f"{message}"),
                                        html.Small("Esperando archivo...", id='output-data-upload')
                                    ]
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.Button("Clean"),
                                html.Button("Click")
                            ]
                        )
                    ]
                )
            ]
        )
    ],
    className="upload__container"
)
