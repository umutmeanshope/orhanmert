import re
import pandas as pd
from collections import namedtuple
from logger import log
import timeit


class DeliveryNote:
    """

    This class is specifically designed to read only one type of delivery note pdf.
    The class is using regular expressions to loop through and recognize the info in the extracted text.

    Info the class looks for is:

    Document number, document date, order number and the list of items delivered.

    List of items delivered also has different info associated with it:

    Item number, name, lot number, remaining shelf life days, best before date and quantity.

    Item data processor can also be further separated into a child class of the DeliveryNote.

    """
    order_line_re = re.compile(r"(\d{4}) (\d{8}) (\d{13}) (.*) (\d+(\.\d*)?) .* ([A-Z]{3}\d{5})")
    name_date_re = re.compile(r"(Nummer) (/) (Datum:)(\d{8}) (/)(\d{2}\.\d{2}\.\d{4})")

    item_line_re = re.compile(r"(\d{6}) (\d{4}) (\d{13}) (.*) (\d+) (.*)")
    lot_line_re = re.compile(r"(\d{8}) (Restlaufzeit\(Tage\)) (\d+) (Charge) (.*)\s?(MHD) (\d{2}\.\d{2}\.\d{4})")

    lot_data = namedtuple("LotData", ["item_number",
                                      "item_name",
                                      "lot_number",
                                      "bbd",
                                      "quantity",
                                      "shelf_life"])

    def __init__(self, text: str):
        """
        :param text: Text extracted from the delivery note pdf
        """

        self.__text = text.split("\n")
        self.doc_number = None
        self.date = None
        self.order_number = None
        self.__assign()  # Call the assign method to populate the attributes with the document info
        self.lot_data_df = self.__process_item_data()

    def __assign(self) -> None:
        """
        Assigns the class instance attributes extracted from delivery note.


        In the instance of no pattern match: None is assigned to the attributes and
        there may be something wrong with the delivery note pdf.

        If there is something wrong with the delivery note. It is good to notice the user of it.
        The delivery notes sent by our supplier is quite cluttered and
        a small piece of info missing likely get unnoticed by humans.
        This way the warehouse team can act faster and reject the delivery note or investigate the missing info.

        :returns: None
        """

        try:

            """
            
            This loop lasts a really short time because all the identifying info of the document is at the top.
            
            When all the info is found the we break out of the loop to save time
            and prevent reassigning the same values over and over.
            
            """

            for line in self.__text:

                # Skip when the doc number and date are found

                if self.doc_number is None and self.date is None:
                    name_date = self.name_date_re.match(line)
                    if name_date:
                        self.doc_number = name_date.group(4)
                        self.date = name_date.group(6)

                # Skip when the order number is found

                elif self.order_number is None:
                    order_line = self.order_line_re.match(line)
                    if order_line:
                        self.order_number = order_line.group(7)

                # Break when all the document info is found, save time

                if self.doc_number and self.date and self.order_number:
                    break

        except Exception as err:
            log.error(f"Error recognizing document date, order number or document id, check the pdf")

    def __process_item_data(self) -> pd.DataFrame:
        """
        Extracts the item data from the delivery note pdf.

        If there's an error during the extracting process there may be a problem with the pdf.

        The item info in the pdf consists of two lines of data for the same item.
        First line has the info such as item number, name, quantity.
        Second line has lot number, shelf life and best before date.
        This complicates the extraction process since the text is split into lines when the class is first created.
        The item info essentially gets cut in half.

        To combat this, the method first recognizes the two item and lot lines and puts them in a list
        alternating between an item line and lot line. Since they are successive in the pdf,
        they are positioned in the list one after the other.

        Next, with the regular expressions, when the method recognizes an "item line" in the new list,
        the line after that is the "lot line" associated with the last "item line".

        Meaning: "index + 1"

        When the cleaning is done, the method starts to extract the item data from the list and puts them in a
        pandas DataFrame.

        Note: The identifier info of the document is on the first and
        the item and lot data start at the second page, in the future, splitting the pages
        and feeding them separately to the methods could be faster and more efficient


        :return: Dataframe with the item data
        """

        start = timeit.default_timer()

        # alternate item and lot lines, put them in a list

        lines = [line for line in self.__text if self.item_line_re.match(line) or self.lot_line_re.match(line)]

        line_items = []

        # classify individual entities in item and lot lines list using regex

        for line, next_line in zip(lines, lines[1:]):
            try:
                if self.item_line_re.match(line):
                    index = lines.index(line)
                    item_line = self.item_line_re.match(line)
                    lot_line = self.lot_line_re.match(next_line)  # Take the index of the previous item line
                    item_number = item_line.group(2)  # the next line will be the "lot line" associated
                    lot_number = lot_line.group(5)  # with the item
                    bbd = lot_line.group(7)
                    quantity = item_line.group(5)
                    shelf_life = lot_line.group(3)
                    item_name = item_line.group(4)
                    line_items.append(self.lot_data(item_number,
                                                    item_name,
                                                    lot_number,
                                                    bbd,
                                                    quantity,
                                                    shelf_life))  # named tuple
            except Exception as e:
                log.error(f"Error extracting lot data {self.doc_number}, Error: {e}")
                log.error(f"Last data extracted {line_items[len(line_items) - 1]}")

        # create a pandas dataframe from the entities

        df = pd.DataFrame(line_items)

        # convert and clean datatypes

        df["item_number"] = pd.to_numeric(df["item_number"])
        df["bbd"] = pd.to_datetime(df["bbd"], dayfirst=True).dt.strftime("%d.%m.%Y")
        df["quantity"] = pd.to_numeric(df["quantity"])
        df["shelf_life"] = pd.to_numeric(df["shelf_life"])

        # Merge the items that has the same lot number and sum their quantity

        final_df = df.groupby(['item_number', 'item_name', 'lot_number', 'bbd', 'shelf_life'],
                              as_index=False)['quantity'].sum()

        end = timeit.default_timer()

        log.info(f"Took {end - start} seconds to process")

        return final_df
