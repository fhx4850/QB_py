import datetime

######### DATABASE ###########
DATABASE_USER = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": 'qb_database',
}

DATABASE_ORM = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "db_log",
}

FIELDS_TAGS = {'add': 'add', 'upd': 'update', 'del': 'delete', 'no': 'no_action'}

ORM_TABLE_NAME = f"mgr-{str(datetime.datetime.today().strftime('%Y-%m-%d_%H:%M:%S'))}"

#### QUERY

ORM_TABLE_QUERY = f'CREATE TABLE `{ORM_TABLE_NAME}` ' \
                  f'(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, ' \
                  f'field_table_name VARCHAR(100) NOT NULL, ' \
                  f'field_name VARCHAR(100) NOT NULL,' \
                  f'type VARCHAR(50) NOT NULL, ' \
                  f'lenght INT NOT NULL, ' \
                  f'isnull BOOLEAN NOT NULL, ' \
                  f'tag VARCHAR(50) NOT NULL)'

ORM_CURRENT_MIGRATION_QUERY = 'CREATE TABLE `current_migration` (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, current_migration VARCHAR(100) NOT NULL)'
ORM_TABLES_QUERY = 'CREATE TABLE `tables` (table_name VARCHAR(100) NOT NULL PRIMARY KEY, tag VARCHAR(50) NOT NULL)'

############################