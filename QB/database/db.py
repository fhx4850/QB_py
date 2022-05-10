from operator import index
import sqlite3
# import sys, os
from mysql.connector import connect, Error

# sys.path.insert(1, os.path.join(sys.path[0], '..'))
from .. import settings
from ..db_fields import *
import json


class DB:
    def __init__(self):
        self.db_name = settings.DATABASEPATH
        try:
            self.connection = connect(host=settings.DATABASE['host'], user=settings.DATABASE['user'],
                                      password=settings.DATABASE['password'], database=settings.DATABASE['database'],
                                      )
        except Error as e:
            self.connection = None
            print(e)

    def __del__(self):
        if self.connection:
            self.connection.close()

    # def _connect(self):
    #     return sqlite3.connect(self.db_name)

    def _close_connect(self):
        self.connect.close()

    def _database_query(self, query: str):
        try:
            cursor = self.connection.cursor()
            print("База данных подключена к SQLite")
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(e)

    def _parse_field_name(self, json_data, table_name, db_data):
        fields_name = []
        _ = json_data[table_name][0]['table_field']
        for i in _:
            fields_name.append(i['field_name'])

        db_field_name = db_data[table_name][0]['table_field'][0]['field_name']

        return fields_name, db_field_name

    def _create_json_table(self, table_name, field_name, field_type, lenght=None, null=False):
        db_data = {
            table_name: [
                {'table_field': [{'field_name': field_name, 'field_type': field_type, 'lenght': lenght, 'null': null,
                                  'commit': 1}]}]
        }
        if null:
            j_null = 'NULL'
        else:
            j_null = 'NOT NULL'
        if os.stat(settings.DBLOGPATH).st_size != 0:
            with open(settings.DBLOGPATH) as db_l:
                json_data = json.load(db_l)

            self._db_log_validaton(json_data, table_name, field_name)

            if not table_name in json_data.keys():
                json_data.update(db_data)

            fields_name, db_field_name = self._parse_field_name(json_data, table_name, db_data)

            if not db_field_name in fields_name:
                json_data[table_name][0]['table_field'].append(
                    {'field_name': field_name, 'field_type': field_type, 'lenght': lenght, 'null': j_null,
                     'commit': 1})
            else:
                for x, i in enumerate(json_data[table_name][0]['table_field']):
                    if field_name == json_data[table_name][0]['table_field'][x]['field_name']:
                        json_data[table_name][0]['table_field'][x]['field_type'] = field_type
                        json_data[table_name][0]['table_field'][x]['lenght'] = lenght
                        json_data[table_name][0]['table_field'][x]['null'] = j_null

            with open(settings.DBLOGPATH, 'w') as db_l:
                json.dump(json_data, db_l, indent=4)
        else:
            with open(settings.DBLOGPATH, 'w') as db_l:
                json.dump(db_data, db_l, indent=4)

    @staticmethod
    def _rename_table(old_name, new_name):
        with open(settings.DBLOGPATH, 'rw') as db_l:
            print(db_l)

    def _db_log_validaton(self, json_data, table_name, field_name):
        if self.table_name in json_data.keys():
            for i in json_data[table_name][0]['table_field']:
                if field_name == i['field_name']:
                    i['commit'] = 1

            with open(settings.DBLOGPATH, 'w') as db_l:
                json.dump(json_data, db_l, indent=4)

    def _search_table_by_name(self, name: str):
        # print("База данных подключена к SQLite")
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SHOW TABLES;")
            result = cursor.fetchall()
            for i in result:
                for j in i:
                    if name == j:
                        return True
            return False
            cursor.close()
        except Error as e:
            print(e)

    def _search_table_column(self, table_name, field_name):
        q = self.custom_query(f'DESC {table_name};')
        for i in q:
            if field_name == i[0] and i[0] != 'id':
                return True
        return False

    def custom_query(self, query: str):
        cursor = self.connection.cursor()
        # print("База данных подключена к SQLite")
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(e)
        cursor.close()

###############################################

# class IntField(DB):
#     def __init__(self, table_name, field_name, lenght, null=False):
#         super().__init__()
#         self.table_name = table_name
#         self.field_name = field_name
#         self.type = 'INTEGER'
#         self.lenght = lenght
#         self.null = null
#         self._create_json_table(self.table_name, self.field_name, self.type, self.lenght, self.null)

###############################################

# class DbInitField(IntField):
#     def __init__(self):
#         self.table_name = self.__class__.__name__
#         self.reset_fields()

#     def __del__(self):
#         self.delete_not_committed_fields()

#     def IntegerField(self, name, lenght, null=False):
#         IntField.__init__(self, self.table_name, name, lenght, null)

#     def reset_fields(self):
#         if os.stat(settings.DBLOGPATH).st_size != 0:
#             with open(settings.DBLOGPATH) as db_l:
#                 json_data = json.load(db_l)
#             if self.table_name in json_data.keys():
#                 for i in json_data[self.table_name][0]['table_field']:
#                     i['commit'] = 0
#                 with open(settings.DBLOGPATH, 'w') as db_l:
#                     json.dump(json_data, db_l, indent=4)

#     def delete_not_committed_fields(self):
#             if os.stat(settings.DBLOGPATH).st_size != 0:
#                 with open(settings.DBLOGPATH) as db_l:
#                     json_data = json.load(db_l)
#             if self.table_name in json_data.keys():
#                 for i in json_data[self.table_name]:
#                     for x, j in enumerate(i['table_field']):
#                         if j['commit'] == 0:
#                             i['table_field'].pop(x)
#                 with open(settings.DBLOGPATH, 'w') as db_l:
#                     json.dump(json_data, db_l, indent=4)

###############################################

# class DbApply(DB):
#     def __init__(self):
#         super().__init__()

#     def __del__(self):
#         return super().__del__()

#     # @classmethod
#     def apply(self):
#         with open(settings.DBLOGPATH) as db_i:
#             db_init = json.load(db_i)
#             __class__._crate_new_db_table(db_init)
#             query = __class__._parse_query()
#             self.test_query(db_init)
#             for i in query:
#                 pass
#                 # self._database_query(i)

#     @classmethod
#     def _crate_new_db_table(self, db_init):
#         create = []
#         for i in db_init:
#             db_dict = {}
#             db_dict['table_name'] = i
#             for j in db_init[i]:
#                 db_dict['table_field'] = j['table_field']
#                 create.append(db_dict)

#         with open(settings.DBQUERYPATH, 'w') as q:
#             db_query = 'CREATE TABLE '
#             for x, i in enumerate(create):
#                 if x == 0:
#                     e = db_query + str(i['table_name'] + '(\nid INTEGER PRIMARY KEY,')
#                 else:
#                     e = '\n\n' + db_query + str(i['table_name'] + '(\nid INTEGER PRIMARY KEY,')
#                 q.write(e)
#                 for x, j in enumerate(i['table_field']):
#                     if j['null']:
#                         null = ' NULL'
#                     else:
#                         null = ' NOT NULL'
#                     if x == len(i['table_field'])-1:
#                         q.write('\n' + str(j['field_name']) + ' ' + str(j['field_type'] + null + ')'))
#                     else:
#                         q.write('\n' + str(j['field_name']) + ' ' + str(j['field_type']) + null + ',')


#     def test_query(self, db_init):
#         create = []
#         for i in db_init:
#             db_dict = {}
#             db_dict['table_name'] = i
#             for j in db_init[i]:
#                 db_dict['table_field'] = j['table_field']
#                 create.append(db_dict)

#         for i in create:
#             tableInDb = self._search_table_by_name(i['table_name'])
#             if tableInDb:
#                 for j in i['table_field']:
#                     if(self._search_table_column(i['table_name'], j['field_name'])):
#                         print(f"ALTER TABLE `{i['table_name']}` CHANGE `{j['field_name']}` `{j['field_name']}` {j['field_type']} NULL")
#                         # 'ALTER TABLE `test_tab` CHANGE `eee` `eee` VARCHAR(11) NOT NULL;'
#                     else:
#                         if j['null']:
#                             # pass
#                             print(f"ALTER TABLE `{i['table_name']}` ADD `{j['field_name']}` {j['field_type']} NULL")
#                         else:
#                             # pass
#                             print(f"ALTER TABLE `{i['table_name']}` ADD `{j['field_name']}` {j['field_type']} NOT NULL")


#     @classmethod
#     def _parse_query(self):
#         with open(settings.DBQUERYPATH, 'r') as q:
#             qr = q.read()
#             query = qr.split('\n\n')
#         return query