
""" A module for Table classes """

from typing import List, Dict

Columns = Dict[
    name: Dict[name: str, type: str],
]

class Table():

    autocommit = False

    def __init__(self, name: str, parentdb: str) -> None:
        """ Initializes Table object """

        self.name = name
        self.parent = parentdb

        #self.columns = self.get_columns()

    #def get_columns(self) -> Columns:
    #    """ Returns a dictionary with column names and types """
    #    pass
