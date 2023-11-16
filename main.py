import fletapp
import flet as ft


def main(page: ft.Page):

    """
    Create the flet app page

    :param page: Page class instance, inserted by flet
    :return: None
    """

    dialog = fletapp.dialog
    # pass the Page object to the dialog object
    dialog.get_page(page)

    page.title = "Orhan Mert"
    page.window_width = 600
    page.window_height = 400
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.overlay.append(fletapp.folder_picker)  # Add the file and folder picker to the overlay
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
