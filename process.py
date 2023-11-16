import os.path
import pdfplumber
import config
from delivery_note import DeliveryNote
import flet as ft
from logger import log
import dialog as dlg

dialog = dlg.Dialog()


def on_result_path(e: ft.FilePickerResultEvent) -> None:
    """
    This function is called by the file picker when the user selects an output directory

    The app asks for an output folder when first run.

    flet file picker has an "on_result" event that is called when user picks a file
    This function that is called to save folder location to the config.json for further use
    and prevent asking the user for an output directory every time when run.

    :param e: FilePickerResultEvent class instance is inserted automatically by flet file picker
    :return:
    """
    config.update_dump_folder(e.path)

# Create folder picker and point to the update directory path function


folder_picker = ft.FilePicker(on_result=on_result_path)


def extract(pdf_file: str, page_number: str = "all") -> str | None:
    """
    Extracts the all text from the pdf into a string

    Only excepts pdf files

    :param pdf_file: file path
    :param page_number: page number to be extracted, all pages will be extracted if not provided
    :return: str or None if error
    """

    try:
        #  extract text from the pdf file
        with pdfplumber.open(pdf_file) as pdf:
            if page_number == "all":  # take all pages
                text = ""
                for page_number in range(len(pdf.pages)):
                    page = pdf.pages[page_number]
                    page_text = page.extract_text()
                    text += page_text + "\n"
                return text
            else:
                page = pdf.pages[int(page_number)]  # take a specific page
                text = page.extract_text()
                return text
    except Exception as e:
        log.error(f"Error extracting file {pdf_file} Error: {e}")


def create_excel(dn: DeliveryNote, dump_folder: str) -> None:
    """
    Creates an Excel file with the given dataframe

    :param dn: Dataframe
    :param dump_folder: Output folder
    :return: None
    """
    try:

        dn.lot_data_df.to_excel(
            f"{dump_folder}\\{dn.order_number}_{dn.doc_number}_{dn.date}.xlsx",
            index=False, engine="openpyxl")
    except Exception as err:
        log.error(f"Error creating excel file: {err}")


def process_delivery_note(text: str) -> None:
    """
    This function is called on the text extracted by the extractor, ideally in a for loop.

    Create a DeliveryNote class to process the info in the pdf
    and create an Excel file containing the item data.
    :param text: Text extracted by the extractor function
    :return: None
    """
    delivery_note = DeliveryNote(text)
    log.info(f"{delivery_note.doc_number} - Started")
    dump_folder = config.get_dump_folder()  # get the output location saved in the config.json

    """
    If there's no saved location, ask the user to select one using the file picker
    
    """

    if dump_folder is None or not os.path.exists(dump_folder):
        folder_picker.get_directory_path()

    create_excel(dn=delivery_note,
                 dump_folder=dump_folder)
    log.info(f"{delivery_note.doc_number} - Done")


def start_process(e: ft.FilePickerResultEvent) -> None:
    """
    This function is called when the user selects file or files to process
    it enters a for loop and processes the files

    ft.FilePickerResultEvent provides the file paths selected by the user in a list

    :param e: FilePickerResultEvent class instance is inserted automatically by flet file picker
    :return: None
    """

    files = e.files

    for file in files:
        path = file.path
        text = extract(path)
        process_delivery_note(text)

    dialog.open_dialog()


"""
Create the file picker and point to the main process function
I created two different file picker instances because the on result events of them is different for both of them

A single file picker can also be created and used by changing its on result event in runtime

I separated them into file picker and folder picker to be organised and neat
"""

file_picker = ft.FilePicker(on_result=start_process)


