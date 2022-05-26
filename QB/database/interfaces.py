from abc import ABCMeta, abstractmethod


class DbInterface(metaclass=ABCMeta):
    @abstractmethod
    def _open_connection(self, db_data: tuple):
        pass

    @abstractmethod
    def _close_connection(self):
        pass


class DbInitInterface(metaclass=ABCMeta):
    @abstractmethod
    def integerField(self, name, lenght, null=False):
        pass

    def charField(self, name, lenght, null=False):
        pass

    def textField(self, name, lenght, null=False):
        pass

    def dateTimeField(self, name, lenght, null=False):
        pass

    def floatField(self, name, lenght, null=False):
        pass

    def booleanField(self, name, lenght, null=False):
        pass
