import flet as ft
import webbrowser

"""
Added a simple dialog class to notify the user when the process is done.

"""


def rick_roll(e) -> None:
    """
    Added a joke if the user presses the "OK" button instead of "Thank you" button lol

    :param e: Flet event passed automatically
    :return: None
    """
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygULbmV2ZXIgZ29ubmE%3D")


class Dialog:

    def __init__(self):

        self.page = None
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Done!"),
            content=ft.Text("Documents Processed."),
            actions=[
                ft.TextButton("OK", on_click=rick_roll),
                ft.TextButton("Thank you", on_click=self.close_dialog)

            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=rick_roll
        )

    def open_dialog(self) -> None:
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close_dialog(self, e) -> None:
        self.dialog.open = False
        self.page.update()

    def get_page(self, page: ft.Page) -> None:
        """
        This method passes the page object from the main.py to the dialog object.

        Called in the main.py folder

        :param page: Page object
        :return: None
        """
        self.page = page




