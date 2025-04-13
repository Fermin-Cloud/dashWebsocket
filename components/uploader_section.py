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
                        dcc.Upload(
                            className="upload",
                            id='upload-data',
                            multiple=False,
                            children=html.Div([
                                html.Strong(f"{message}"),
                                html.Small("Esperando archivo...", id='output-data-upload'),
                            ])
                        ),
                        html.Div(
                            [
                                html.Progress(value=0, max=100, id='upload-progress'),
                                html.Div(
                                    [
                                        html.Button([html.Span("⏸")], id='pause-btn', type="button"),
                                        html.Button([html.Span("▶")], id='resume-btn', type="button"),
                                        html.Button([html.Span("✖")], id='cancel-btn', type="button"),
                                    ],
                                )
                            ], className="upload--buttons"
                        ),
                        html.Footer(
                            [
                                html.Button("🧹 Limpiar", id='clean-btn', type="button"),
                                html.Button("⬆ Subir", id='upload-btn', type="button"),
                            ]
                        ),
                    ]
                )
            ]
        )
    ],
    className="upload__container"
)
