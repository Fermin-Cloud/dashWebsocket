"""
# bnjmn - bastudillo.alarcon@gmail.com
#
# upload and websocket component
"""

from dash import html, dcc

message: int = 'Arrastra y suelta o haz clic para seleccionar'

upload_section = html.Section(
    [
        html.Form(
            [
                html.Fieldset(
                    [
                        html.Legend("Subida de Archivos con Progreso (Drag & Drop): "),
                        html.Label(
                            [
                                dcc.Upload(
                                    id='upload-data',
                                    children=html.Div(
                                        [
                                            html.Strong(f"{message}"),
                                            html.Small(id='output-data-upload')
                                        ]
                                    ),
                                    multiple=False,
                                    className="upload-data"
                                )
                            ]
                        ),
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
