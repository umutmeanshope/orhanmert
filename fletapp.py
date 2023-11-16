import flet as ft
import process as pr

dialog = pr.dialog

"""

Since this was a quick project that my coworker needed it fast 
I only added two buttons to process the pdf files and setting an output folder

To do: A notification panel can be added to notify the user of the 
process and some error windows to alert the user of errors.

"""

file_picker = pr.file_picker
folder_picker = pr.folder_picker


"""
This button asks the user for files to process and 
calls the process function when user selects files
"""

process_button = ft.ElevatedButton(
    text="Start Process",
    width=200,
    height=50,
    on_click=lambda _: file_picker.pick_files(
        dialog_title="Select files to process",
        allow_multiple=True,
        )
)

"""

This button gets the output directory from the user and 
saves it in a config.json file

An output directory is also asked when the app is first run.

"""
dump_folder_button = ft.ElevatedButton(
    text="Output Folder",
    width=150,
    height=45,
    on_click=lambda _: folder_picker.get_directory_path(dialog_title="Select an output folder")
)


# stack the buttons vertically in a column

button_column = ft.Column(
    [
        process_button,
        dump_folder_button
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)

button_container = ft.Container(content=button_column)






