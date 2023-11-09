import os.path
from datetime import date
import pandas as pd
import pdfplumber

import config
from delivery_note import DeliveryNote
import flet as ft
from logger import log


def on_result_path(e: ft.FilePickerResultEvent):
    config.update_dump_folder(e.path)


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
    try:

        dn.lot_data_df.to_excel(
            f"{dump_folder}\\{dn.order_number}_{dn.doc_number}_{dn.date}.xlsx",
            index=False, engine="openpyxl")
    except Exception as err:
        log.error(f"Error creating excel file: {err}")

def process_delivery_note(text: str):

    delivery_note = DeliveryNote(text)
    log.info(f"{delivery_note.doc_number} - Started")
    dump_folder = config.get_dump_folder()

    if not config.dump_folder_set() or not os.path.exists(dump_folder):
        folder_picker.get_directory_path()

    create_excel(dn=delivery_note,
                 dump_folder=dump_folder)
    log.info(f"{delivery_note.doc_number} - Done")


def start_process(e: ft.FilePickerResultEvent):

    files = e.files

    for file in files:
        path = file.path
        text = extract(path)
        process_delivery_note(text)


file_picker = ft.FilePicker(on_result=start_process)



