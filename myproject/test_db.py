from QB.database.fields.object import DbInit


class TestTab6(DbInit):
    def __init__(self):
        super().__init__()
        self.charField('profile_name_1', 100)
        self.integerField('qqqq', 200, null=True)
        self.charField('qw', 6, null=True)


# class QB(DbInit):
#     def __init__(self):
#         super().__init__()
#         self.integerField('qb', 100)
#         self.charField('hello', 200)
#         # self.charField('Hello_w', 200)


class TestTwo(DbInit):
    def __init__(self):
        super().__init__()
        self.textField('two', 100)
        self.textField('three', 100)