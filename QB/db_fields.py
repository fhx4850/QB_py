# from .db import DB

class IntField:
    def __init__(self, table_name, field_name, lenght, null=False):
        super().__init__()
        self.table_name = table_name
        self.field_name = field_name
        self.type = 'int'
        self.lenght = lenght
        self.null = null
        self.create_field(self.table_name, self.field_name, self.type, self.lenght, self.null)

    def __str__(self):
        return self.create_field(self.table_name, self.field_name, self.type, self.lenght, self.null)

    # def IntegerField(self, name, lenght, null=False):
    #     print(self.table_name)