from mysql.connector import connect, Error
from QB.database.interfaces import DbInterface


class DB(DbInterface):
    """
    Database interaction class.
    """
    def __init__(self, db_data: dict):
        """
        Parameters
        ----------
        db_data : dict
            Data to connect to the database.
        """
        self.connection = None
        self.base_connection = None
        self.db_data = db_data

    def __del__(self):
        self._close_connection()
        self._close_base_connection()

    def get_connection(self):
        return self.connection

    def _open_base_connection(self, db_data: dict):
        """
        Opens a connection without being bound to a database.

        Parameters
        ----------
        db_data : dict
            Data to connect to the database.
        """
        try:
            self.base_connection = connect(host=db_data['host'], user=db_data['user'],
                password=db_data['password']
            )
            return self.base_connection
        except Error as e:
            self.base_connection = None
            print(e)

    def _open_connection(self, db_data: dict):
        """
        Opens a connection to a specific database.

        Parameters
        ----------
        db_data : dict
            Data to connect to the database.
        """
        try:
            self.connection = connect(host=db_data['host'], user=db_data['user'],
                password=db_data['password'], database=db_data['database']
            )
            return self.connection
        except Error as e:
            self.connection = None
            print(e)

    def _close_connection(self):
        """
        Closes the connection to the database.

        Returns
        -------
        None
        """
        if self.connection:
            self.connection.close()

    def _close_base_connection(self):
        """
        Closes base connection.

        Returns
        -------
        None
        """
        if self.base_connection:
            self.base_connection.close()