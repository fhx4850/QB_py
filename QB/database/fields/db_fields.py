
class Field:
    def __init__(self, table_name, field_name, type, lenght, null):
        self.table_name = table_name
        self.field_name = field_name
        self.type = type
        self.lenght = lenght
        self.null = null

    def get_field_table_name(self):
        return self.table_name.lower()

    def get_field_name(self):
        return self.field_name

    def get_field_type(self):
        return self.type

    def get_field_lenght(self):
        return self.lenght

    def get_field_isnull(self):
        return self.null


class IntField(Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        self.type = 'INT'
        super().__init__(table_name, field_name, self.type, lenght, null)


class CharField(Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        self.type = 'VARCHAR'
        Field.__init__(self, table_name, field_name, self.type, lenght, null)


class TextField(Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        self.type = 'TEXT'
        Field.__init__(self, table_name, field_name, self.type, lenght, null)


class DateTimeField(Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        self.type = 'DATETIME'
        Field.__init__(self, table_name, field_name, self.type, lenght, null)


class FloatField(Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        self.type = 'FLOAT'
        Field.__init__(self, table_name, field_name, self.type, lenght, null)


class BooleanField(Field):
    def __init__(self, table_name, field_name, lenght, null=False):
        self.type = 'BOOLEAN'
        Field.__init__(self, table_name, field_name, self.type, lenght, null)