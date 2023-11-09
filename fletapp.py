import flet as ft
import process as pr


file_picker = pr.file_picker
folder_picker = pr.folder_picker

process_button = ft.ElevatedButton(
    text="Start Process",
    width=200,
    height=50,
    on_click=lambda _: file_picker.pick_files(
        dialog_title="Select files to process",
        allow_multiple=True
        )
)

dump_folder_button = ft.ElevatedButton(
    text="Output Folder",
    width=150,
    height=45,
    on_click=lambda _: folder_picker.get_directory_path(dialog_title="Select an output folder")
)


button_column = ft.Column(
    [
        process_button,
        dump_folder_button
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)

button_container = ft.Container(content=button_column)






