# layout.py
from dash import html
from components.uploader_section import upload_section
from components.commands_section import command_section

layout = html.Main([
    upload_section,
    command_section,
], className="main__container")