from QB.database.db import DB


class Field:
    def __init__(self, table_name, field_name, lenght, null):
        self.table_name = table_name
        self.field_name = field_name
        # self.type = 'INTEGER'
        self.lenght = lenght
        self.null = null


class IntField(DB, Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        Field.__init__(Field, table_name, field_name, lenght, null=False)
        self.type = 'INTEGER'
        self._create_json_table(self.table_name, self.field_name, self.type, self.lenght, self.null)

    def __repr__(self):
        return 'cecececcecece'


class CharField(DB, Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        Field.__init__(Field, table_name, field_name, lenght, null=False)
        self.type = 'VARCHAR'
        self._create_json_table(self.table_name, self.field_name, self.type, self.lenght, self.null)