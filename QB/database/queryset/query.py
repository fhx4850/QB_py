from QB.database.configuration.db import DB
from mysql.connector import Error


class Query(DB):
    """
    The class is used to create and execute database queries.
    """
    def __init__(self, db_data: dict):
        super().__init__(db_data)
        self.cursor = None
        self.conn = None

    def custom_query(self, query: str, db_connection=False, base_connection=False, dictionary=False):
        """
        Executes a database query. Returns request data.

        Parameters
        ----------
        query : str
            Request text.
        db_connection: bool
            Connection to a specific database.
        base_connection: bool
            Connection not tied to a database.
        dictionary: bool
            Output the response data to the request in the form of a dictionary.
        Notes
        -------
        One of the db_connection or base_connection arguments must be True.
        Returns
        -------
        list
        """
        if db_connection:
            self.__custom_db_connection(dictionary)
        if base_connection:
            self.__custom_base_connection(dictionary)
        if not db_connection and not base_connection:
            raise 'Not connection from custom_query!'
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.conn.commit()
            self.cursor.close()
            self._close_connection()
            self._close_base_connection()
            return result
        except Error as e:
            print(e)
            self._close_connection()
            self._close_base_connection()
            self.cursor.close()

    def __custom_db_connection(self, dictionary):
        """
        Opens a connection to the database.

        Parameters
        ----------
        dictionary: bool
            Output the response data to the request in the form of a dictionary.
        Returns
        -------
        None
        """
        self._open_connection(self.db_data)
        self.conn = self.connection
        self.cursor = self.connection.cursor(dictionary=dictionary)

    def __custom_base_connection(self, dictionary):
        """
        Opens a connection without being bound to a database.

        Parameters
        ----------
        dictionary: bool
            Output the response data to the request in the form of a dictionary.
        Returns
        -------
        None
        """
        self._open_base_connection(self.db_data)
        self.conn = self.base_connection
        self.cursor = self.base_connection.cursor(dictionary=dictionary)

    def search_field_data(self, table_name, column_name, search_value):
        """
        Searches for specific data in a specific table and column.

        Parameters
        ----------
        table_name: str
            The name of the table to search.
        column_name: str
            The name of the column to search.
        search_value: str
            Search data.
        Returns
        -------
        bool
        """
        q = self.custom_query(f'SELECT {column_name} FROM `{table_name}`', db_connection=True, dictionary=True)
        value = str([i[column_name] for i in q])
        if search_value in value:
            return True
        return False

    def search_table_by_name(self, name: str):
        """
        Searches for a table in the database by name.

        Parameters
        ----------
        name
            Table name.
        Returns
        -------
        bool
        """
        try:
            result = self.custom_query(f"SHOW TABLES;", db_connection=True)
            for i in result:
                for j in i:
                    if name.lower() in j:
                        return True
            return False
        except Error as e:
            print(e)

    def search_db_by_name(self, name: str):
        """
        Searches for a database by name.

        Parameters
        ----------
        name
            Database name.
        Returns
        -------
        bool
        """
        try:
            result = self.custom_query(f"SHOW DATABASES;", base_connection=True)
            for i in result:
                for j in i:
                    if name in j:
                        return True
            return False
        except Error as e:
            print(e)

    def insert_field_data(self, table_name, fields: dict):
        # print(table_name)
        # print(fields)
        """
        Adds data to a table.

        Parameters
        ----------
        table_name: str
        fields: dict
            Accepts a dictionary of type column name - value.
        Returns
        -------
        None
        """
        fields_name = []
        fields_value = []
        for i in fields.items():
            fields_name.append(i[0])
            fields_value.append(i[1])
        query = f'INSERT INTO `{table_name}` ('
        for x, i in enumerate(fields_name):
            if x == len(fields_name)-1:
                query += str(f' `{i}`) VALUES (')
            else:
                query += str(f' `{i}`,')
        for x, i in enumerate(fields_value):
            if x == len(fields_value) - 1:
                query += f" '{i}')"
            else:
                query += f" '{i}',"
        self.custom_query(query, db_connection=True)

    def create_table(self, table_name, table_query):
        """
        Creates a table if it does not exist in the database.

        Parameters
        ----------
        table_name: str
        table_query: str
            The full text of the request to create a table.
        Notes
        -------
        You must create at least one column in your query. Most often it is id.
        Returns
        -------

        """
        try:
            if not self.search_table_by_name(table_name):
                result = self.custom_query(table_query, db_connection=True)
                print(f'✓ Succsess created table {table_name}')
                return result
        except Exception as e:
            print(e)

    def create_db(self, db_name: str):
        """
        Creates a database if it doesn't already exist.

        Parameters
        ----------
        db_name:str

        Returns
        -------

        """
        try:
            if not self.search_db_by_name(db_name):
                cq = self.custom_query(f'CREATE DATABASE {db_name}', base_connection=True)
                print(f'✓ Succsess created database {db_name}')
                return cq
        except Exception as e:
            print(e)

    def select_tables(self, value, table_name, dictionary=False):
        """

        Parameters
        ----------
        value: str
            The value to select.
        table_name: str
        dictionary: bool
            Output the response data to the request in the form of a dictionary.
        Returns
        -------
        list
        """
        return self.custom_query(f'SELECT {value} FROM `{table_name}`', db_connection=True, dictionary=dictionary)

    def select_tables_ob(self, table_name, order_by, value='*', desc=False, dictionary=False):
        if desc:
            return self.custom_query(f'SELECT {value} FROM `{table_name}` ORDER BY {order_by} DESC', db_connection=True, dictionary=dictionary)
        else:
            return self.custom_query(f'SELECT {value} FROM `{table_name}` ORDER BY {order_by}', db_connection=True,
                                     dictionary=dictionary)

    def select_tables_w(self, value, table_name, where, dictionary=False):
        """

        Parameters
        ----------
        value: str
            The value to select.
        table_name: str
        where: str
            The condition for the selection.
        dictionary: bool
            Output the response data to the request in the form of a dictionary.
        Returns
        -------
        list
        """
        return self.custom_query(f'SELECT {value} FROM `{table_name}` WHERE {where}', db_connection=True, dictionary=dictionary)

    def add_columns(self, table_name, column_name, type, lenght, isnull):
        """
        Adds a column to the table.

        Parameters
        ----------
        table_name: str
        column_name: str
        type: str
        lenght: int
        isnull: bool

        Returns
        -------
        None
        """
        if isnull == 0:
            null = 'NULL'
        else:
            null = 'NOT NULL'
        query = f'ALTER TABLE `{table_name}` ADD `{column_name}` {type}({lenght}) {null};'
        self.custom_query(query, db_connection=True)

    def update_colums(self, table_name, column_name, type, lenght, isnull):
        """
        Updates a column in a table.

        Parameters
        ----------
        table_name: str
        column_name: str
        type: str
        lenght: int
        isnull: bool

        Returns
        -------
        None
        """
        if isnull == 0:
            null = 'NULL'
        else:
            null = 'NOT NULL'
        query = f'ALTER TABLE `{table_name}` CHANGE `{column_name}` `{column_name}` {type}({lenght}) {null}'
        self.custom_query(query, db_connection=True)

    def describe_field(self, table_name):
        """
        Returns data about the selected table.

        Parameters
        ----------
        table_name: str

        Returns
        -------
        list
        """
        return self.custom_query(f'DESCRIBE {table_name}', db_connection=True, dictionary=True)

    def show_tables(self):
        return self.custom_query('SHOW TABLES', db_connection=True)

    def foreign_key(self, alter_table, a_column, ref_table, ref_column, on_delete='CASCADE', on_update='RESTRICT'):
        """
        Creates a connection foreign key.

        Parameters
        ----------
        alter_table: str
        a_column: str
            The column to which the binding is made.
        ref_table: str
            The table that contains the column to bind to.
        ref_column: str
             Binding column.
        on_delete: str
        on_update: str

        Returns
        -------
        None
        """
        query = f'ALTER TABLE `{alter_table}` ADD FOREIGN KEY (`{a_column}`) REFERENCES `{ref_table}`(`{ref_column}`) ON DELETE {on_delete} ON UPDATE {on_update};'
        self.custom_query(query, db_connection=True)

    def delete_row(self, from_table, column, row_data):
        """

        Parameters
        ----------
        from_table: str
        column: str
        row_data: str

        Returns
        -------

        """
        query = f"DELETE FROM `{from_table}` WHERE {column}='{row_data}';"
        self.custom_query(query, db_connection=True)

    def update_field(self, table_name, column_name, value, pk_name, pk_value):
        """

        Parameters
        ----------
        table_name: str
        column_name: str
        value: str
            The new row value in the selected column.
        pk_name:
            The table's primary key.
        pk_value:
            The value of the primary key to search for the string.
        Returns
        -------
        None
        """
        query = f"UPDATE `{table_name}` SET `{column_name}` = '{value}' WHERE `{table_name}`.`{pk_name}` = '{pk_value}';"
        self.custom_query(query, db_connection=True)

    def delete_table_data(self, table_name):
        self.custom_query(f'TRUNCATE TABLE {table_name};', db_connection=True)

    def get_columns(self, table_name, dictionary=False):
        """
        Returns data about the columns of the selected table.

        Parameters
        ----------
        table_name: str
        dictionary: bool
            Output the response data to the request in the form of a dictionary.
        Returns
        -------
        list
        """
        return self.custom_query(f"SHOW columns FROM {table_name};", db_connection=True, dictionary=dictionary)

    def delete_column(self, table_name, column_name):
        self.custom_query(f"ALTER TABLE `{table_name}` DROP `{column_name}`;", db_connection=True)

    def delete_table(self, table_name):
        self.custom_query(f'DROP TABLE `{table_name}`', db_connection=True)

    def change_table_name(self, old_table_name, new_table_name):
        if self.search_table_by_name(old_table_name):
            self.custom_query(f'ALTER TABLE `{old_table_name}` RENAME TO `{new_table_name}`', db_connection=True)