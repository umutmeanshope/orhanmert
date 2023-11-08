import flet as ft
import config
from tkinter import filedialog
import process as pr

process_button = ft.ElevatedButton(text="Start Process",
                                   width=200,
                                   height=50)


dump_folder_button = ft.ElevatedButton(text="Output Folder",
                                       width=150,
                                       height=45,
                                       on_click=pr.update_dump_folder)


button_column = ft.Column(
    [
        process_button,
        dump_folder_button
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)

button_container = ft.Container(content=button_column)






