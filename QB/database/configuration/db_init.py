from QB.database.fields.db_fields import *
from QB.database.configuration.orm import DbOrm
from QB.database.interfaces import DbInitInterface


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
