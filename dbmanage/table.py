
""" A module for Table classes """

from typing import List, Dict

ColumnDict = Dict[str, List[str]]

class Table():

    autocommit = False

    def __init__(self, name: str, parentdb: str) -> None:
        """ Initializes Table object """

        self.name = name
        self.parent = parentdb

        self.columns = self.get_columns()

    def get_columns(self) -> ColumnDict:
        """ Returns a dictionary with column names and types """

        columns: ColumnDict
        columns = dict()
        return columns
