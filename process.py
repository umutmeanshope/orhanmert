from datetime import date
import pandas as pd
import pdfplumber

import config
from delivery_note import DeliveryNote
from tkinter import filedialog

def update_dump_folder(e):
    config.update_dump_folder(filedialog.askdirectory(title="Select dump folder"))


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
        print(f"Error extracting pdf file {pdf_file} Error: {e}")


def create_excel(df: pd.DataFrame, dump_folder: str, dn: DeliveryNote) -> None:

    df.to_excel(
        f"{dump_folder}{dn.order_number}_{dn.doc_number}_{date.strftime(dn.date, '%d.%m.%Y')}.xlsx",
        index=False)



