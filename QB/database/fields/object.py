from QB.database.fields.db_fields import *
from QB.database.configuration.orm import DbOrm
from QB.database.interfaces import DbInitInterface
from QB.database.queryset.query import Query as Qr
from QB.settings import base_settings as bs


class DbInit(DbOrm, DbInitInterface):
    def __init__(self):
        super().__init__()
        self.table_name = self.__class__.__name__

    log_table_name = None

    def integerField(self, name, lenght, null=False):
        integer = IntField(self.table_name, name, lenght, null)
        self.append_field(integer)

    def charField(self, name, lenght, null=False):
        charfield = CharField(self.table_name, name, lenght, null)
        self.append_field(charfield)

    def textField(self, name, lenght, null=False):
        textfield = TextField(self.table_name, name, lenght, null)
        self.append_field(textfield)

    def dateTimeField(self, name, lenght, null=False):
        dateTimeField = DateTimeField(self.table_name, name, lenght, null)
        self.append_field(dateTimeField)

    def floatField(self, name, lenght, null=False):
        floatField = FloatField(self.table_name, name, lenght, null)
        self.append_field(floatField)

    def booleanField(self, name, lenght, null=False):
        booleanField = BooleanField(self.table_name, name, lenght, null)
        self.append_field(booleanField)


class Dobj:
    """
    The class represents a table from a user database.
    """
    def __init__(self, table_name):
        self._table_name = table_name
        self._qr = Qr(bs.DATABASE_USER)
        self._field_name = None
        self._received_field = None

    def __repr__(self):
        if self._field_name:
            return str(self._table_name) + ', ' + str(self._field_name)
        else:
            return self._table_name

    def all(self):
        """
        Returns all fields from the selected table.

        Returns
        -------
        list
        """
        return self._qr.select_tables('*', self._table_name, dictionary=True)

    def all_order_by(self, column, desc=False):
        """
        Returns all fields of the selected table, sorted by the selected column.

        Parameters
        ----------
        column: str
        desc: bool
            Expand sorting.

        Returns
        -------
        list
        """
        return self._qr.select_tables_ob(self._table_name, column, desc=desc, dictionary=True)

    def get(self, **kwargs):
        """
        Returns an object of type _DobjField that represents a single field.

        Parameters
        ----------
        kwargs
            Accepts the primary key of the field (most often id) and its value.
        Returns
        -------
        _DobjField | None
        """
        key = list(kwargs.keys())
        val = None
        if type(kwargs[key[0]]) == int:
            val = kwargs[key[0]]
        elif type(kwargs[key[0]]) == str:
            val = f"'{kwargs[key[0]]}'"
        if self._qr.search_field_data(self._table_name, key[0], str(val)):
            return _DobjField(self._table_name, kwargs, self._qr.select_tables_w('*', self._table_name, f"`{key[0]}`={val}", dictionary=True)[0])
        else:
            return None

    def create(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
            Accepts data of type field name-value.
        Returns
        -------
        None
        """
        self._qr.insert_field_data(self._table_name, kwargs)

    def filter(self, **kwargs):
        """
        Display fields based on selected arguments.

        Parameters
        ----------
        kwargs
            Accepts data of type field name-value.
        Returns
        -------
        list
        """
        k = str(*kwargs)
        k_value = kwargs[k]
        return self._qr.select_tables_w('*', self._table_name, f"`{k}`='{k_value}'", dictionary=True)


class _DobjField:
    """
    The class represents a specific field of the selected table.
    """
    def __init__(self, table_name, get, field: dict):
        """

        Parameters
        ----------
        table_name: str
        get: dict
            The arguments to the get method.
        field: str
            Field data.
        """
        self._field = field
        self._table_name = table_name
        self._get = get
        self._qr = Qr(bs.DATABASE_USER)

    def __repr__(self):
        return str(self._field)

    def get_attr(self, attr):
        """

        Parameters
        ----------
        attr: str
            Column name.
        Returns
        -------
        str
        """
        return self._field[attr]

    def update(self, **kwargs):
        k = str(*kwargs)
        k_value = kwargs[k]
        pk = str(*self._get)
        pk_value = self._get[str(*self._get)]
        self._qr.update_field(self._table_name, k, k_value, pk, pk_value)

    def delete(self):
        pk = str(*self._get)
        pk_value = self._get[str(*self._get)]
        self._qr.delete_row(self._table_name, pk, pk_value)