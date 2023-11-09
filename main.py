import fletapp
import flet as ft


def main(page: ft.Page):

    page.title = "Orhan Mert"
    page.window_width = 600
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.overlay.append(fletapp.folder_picker)
    page.overlay.append(fletapp.file_picker)
    page.update()


    page.add(
        ft.Row(
            [
                fletapp.button_column
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
