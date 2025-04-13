from dash import ClientsideFunction, Input, Output, clientside_callback, html, dcc

message: str = 'Arrastra y suelta o haz clic para seleccionar'
title: str = 'Subida de Archivos con progreso: Drag & drop'

upload_section = html.Section(
    [
        html.Form(
            [
                html.Fieldset(
                    [
                        html.Legend(f"{title}"),
                        html.Label([
                            dcc.Input(
                                id='upload-data',
                                multiple=False,
                                type="file"
                            ),
                            html.Div([
                                    html.Strong(f"{message}"),
                                    html.Small("Esperando archivo...", id='output-data-upload'),
                                ]),
                        ], className="upload"),
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
                                html.Button("🧹 Clean", id='clean-btn', type="button"),
                                html.Button("⬆ Upload", id='upload-btn', type="button"),
                            ]
                        ),
                    ]
                )
            ]
        )
    ],
    className="upload__container"   
)

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='show_selected_filename'
    ),
    Output('output-data-upload', 'children'),
    Input('upload-data', 'value'),  
)

clientside_callback(
    ClientsideFunction(namespace='uploadNS', function_name='handleUpload'),
    # Output('output-data-upload', 'children'),
    Input('upload-btn', 'n_clicks')
)
