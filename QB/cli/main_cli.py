from QB.server.server import IpTcpServer
import project_settings
from QB.database.configuration.db_init import DbInit
from QB.database.configuration.orm import DbOrm
import importlib
# from QB.database.queryset.query import Query
# from QB import settings


class Cli:
    def __init__(self):
        self.db_orm = DbOrm()

    def migrate(self):
        for i in project_settings.apps:
            importlib.import_module(f'{i}.test_db')

        commit_db = DbInit.__subclasses__()

        self.db_orm.create_db_log()
        log_table_name = self.db_orm.create_log_table()
        DbInit.log_table_name = log_table_name
        for db in commit_db:
            db()
        self.db_orm.fields_tag_validation()

    def startserver(self, host='127.0.0.1', port=8888):
        serv = IpTcpServer(host, int(port))
        print(f'Server started on {host}:{port}')
        serv.run()

    def applymigrations(self):
        self.db_orm.apply()
