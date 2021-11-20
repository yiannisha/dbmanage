
""" A module for the Database classes """

from typing import List

class Database():

    def __init__(dbtype: str, dbname: str) -> None:
        """ Initializes a Database object """

        self.dbtype = dbtype
        self.name = dbname
        #self.tables = self.get_tables()

    #def get_tables(self) -> List[Table]:
    #    """ Returns a list of Table objects """
    #    pass
