import fletapp
import flet as ft

def main(page: ft.Page):

    page.title = "Delivery Note Process"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    page.add(
        ft.Row(
            [
                fletapp.button_column
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


if __name__ == '__main__':
    ft.app(target=main)
