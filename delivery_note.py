import re
from datetime import date
import pandas as pd
from collections import namedtuple
from logger import log



class DeliveryNote:

    def __init__(self, text: str):
        """
        :param text: Text extracted from the delivery note pdf
        """

        self.__text = text.split("\n")
        self.doc_number = None
        self.date = None
        self.order_number = None
        self.lot_data_df = self.__process_lot_data()

        self.__assign()

    def __assign(self) -> None:
        """
        Assigns the class instance attributes extracted from delivery note.


        In the instance of no pattern match: None is assigned to the attributes and
        there may be something wrong with the delivery note pdf
        :returns: None
        """

        order_line_re = re.compile(r"(\d{4}) (\d{8}) (\d{13}) (.*) (\d+(\.\d*)?) .* ([A-Z]{3}\d{5})")
        name_date_re = re.compile(r"(Nummer) (/) (Datum:)(\d{8}) (/)(\d{2}\.\d{2}\.\d{4})")

        try:

            for line in self.__text:

                if self.doc_number is None and self.date is None:
                    name_date = name_date_re.match(line)
                    if name_date:
                        self.doc_number = name_date.group(4)
                        self.date = name_date.group(6)

                elif self.order_number is None:
                    order_line = order_line_re.match(line)
                    if order_line:
                        self.order_number = order_line.group(7)

                if self.doc_number and self.date and self.order_number:
                    break
        except Exception as err:
            log.error(f"Error recognizing document date, order number, or document id, check the pdf")

    def __process_lot_data(self) -> pd.DataFrame:
        """
        Extracts the item data from the delivery note pdf

        If there's an error during the extracting process there may be a problem with the pdf

        :return:
        """

        lot_line_re = re.compile(r"(\d{8}) (Restlaufzeit\(Tage\)) (\d+) (Charge) (.*)\s?(MHD) (\d{2}\.\d{2}\.\d{4})")
        item_line_re = re.compile(r"(\d{6}) (\d{4}) (\d{13}) (.*) (\d+) (.*)")

        lot_data = namedtuple("LotData", ["item_number",
                                          "item_name",
                                          "lot_number",
                                          "bbd",
                                          "quantity",
                                          "shelf_life"])

        lines = []
        for line in self.__text:  # alternate item and lot lines, put them in a list
            items = item_line_re.match(line)
            lots = lot_line_re.match(line)
            if items:
                lines.append(line)
            elif lots:
                lines.append(line)

        line_items = []

        for line in lines:  # classify individual entities in item and lot lines list using regex
            try:
                if item_line_re.match(line):
                    index = lines.index(line)
                    item_line = item_line_re.match(line)
                    lot_line = lot_line_re.match(lines[index + 1])  # take the index of the item line, the next line
                    item_number = item_line.group(2)  # will be the lot number line of the item
                    lot_number = lot_line.group(5)
                    bbd = lot_line.group(7)
                    quantity = item_line.group(5)
                    shelf_life = lot_line.group(3)
                    item_name = item_line.group(4)
                    line_items.append(lot_data(item_number,
                                               item_name,
                                               lot_number,
                                               bbd,
                                               quantity,
                                               shelf_life))  # named tuple
            except Exception as e:
                log.error(f"Error extracting lot data {self.doc_number}, Error: {e}")
                log.error(f"Last data extracted {line_items[len(line_items) - 1]}")

        df = pd.DataFrame(line_items)  # create a tabular dataframe from the entities

        df["item_number"] = pd.to_numeric(df["item_number"])  # convert and clean datatypes
        df["bbd"] = pd.to_datetime(df["bbd"], dayfirst=True)
        df["bbd"] = df["bbd"].dt.strftime("%d.%m.%Y")
        df["quantity"] = pd.to_numeric(df["quantity"])
        df["shelf_life"] = pd.to_numeric(df["shelf_life"])

        final_df = df.groupby(['item_number', 'item_name', 'lot_number', 'bbd', 'shelf_life'],
                              as_index=False)['quantity'].sum()

        return final_df



