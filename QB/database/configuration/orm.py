from QB.database.queryset.query import Query
from QB.settings import base_settings as bs


class DbOrm:
    """
    The class represents the ORM implementation algorithms for the database.
    """
    def __init__(self):
        self._field_instance = None
        self.__query = Query(bs.DATABASE_ORM)

    # список полів з таблиць
    __append_fields_collection = []

    # назви таблиць
    __tables_names = set()

    def get_tables_names(self):
        """
        Returns the name of all tables to be migrated.

        Returns
        -------
        set
        """
        return self.__tables_names

    def get_current_migration_name(self):
        """
        Returns the name of the current migration from the "current_migration" table.

        Returns
        -------
        str | None
        """
        cm = self.__query.select_tables('current_migration', 'current_migration')
        if cm:
            return cm[0][0]
        else:
            return None

    def get_append_fields_collection(self):
        """
        Returns a collection of current migration fields.

        Returns
        -------
        list
        """
        return self.__append_fields_collection

    def create_db_log(self):
        """
        Creates a database and tables for the correct functioning of migrations. Typically, used at the start of a
        migration algorithm.

        Returns
        -------
        None
        """
        self.__query.create_db(bs.DATABASE_ORM['database'])
        self.__query.create_table('tables', bs.ORM_TABLES_QUERY)
        self.__query.create_table('current_migration', bs.ORM_CURRENT_MIGRATION_QUERY)

    def create_log_table(self):
        """
        Creates a table to record migrations. Returns the name of the table.

        Returns
        -------
        str
        """
        self.__query.create_table(bs.ORM_TABLE_NAME, bs.ORM_TABLE_QUERY)
        self.__query.foreign_key(bs.ORM_TABLE_NAME, 'field_table_name', 'tables', 'table_name')
        return bs.ORM_TABLE_NAME

    def get_append_fields(self):
        """
        Collects data about table fields and returns that data.
        """
        create_table_name = self._field_instance.get_field_table_name()
        field_name = self._field_instance.get_field_name()
        type = self._field_instance.get_field_type()
        lenght = self._field_instance.get_field_lenght()
        null = self._field_instance.get_field_isnull()
        fields = {}
        fields['field_table_name'] = create_table_name
        fields['field_name'] = field_name
        fields['type'] = type
        fields['lenght'] = lenght
        if null:
            fields['isnull'] = 0
        else:
            fields['isnull'] = 1
        fields['tag'] = None
        return fields

    def append_field(self, field):
        """
        The method is used to collect information from the fields of the database view class.

        Parameters
        ----------
        field
            An instance of the "Field" class.
        Returns
        -------
        None
        """
        self._field_instance = field

        # додає нову назву таблиці до self.__tables_names
        self._set_tables_names(field.get_field_table_name())

        # якщо таблиці не існує у базі даних - додає її
        if not self.__query.search_field_data('tables', 'table_name', field.get_field_table_name()):
            self.__query.insert_field_data('tables', {'table_name': field.get_field_table_name(), 'tag': bs.FIELDS_TAGS['no']})

        fields = self.get_append_fields()
        self._set_append_fields_collection(fields)

    def get_orm_table_name(self):
        """
        Returns the last created migration table.

        Returns
        -------
        str
        """
        all_tables_names_query = self.__query.custom_query('SHOW TABLES', db_connection=True)
        tables_names = [i[0] for i in all_tables_names_query if 'mgr' in i[0]]
        orm_table_name = str(tables_names[len(tables_names) - 1])
        return orm_table_name

    def fields_tag_validation(self):
        """
        The method validates the tags in the fields and writes them to the appropriate tables.

        Returns
        -------
        None
        """
        self.__set_delete_tag_tables()

        # під час першої міграції або якщо міграція не застосована теги не будуть застосовані
        if len(self.__query.show_tables()) <= 1 or not self.get_current_migration_name():
            fields = self.get_append_fields_collection()
            for i in fields:
                i['tag'] = bs.FIELDS_TAGS['no']
                self.__query.insert_field_data(self.get_orm_table_name(), i)
        else:
            # валідація тегів якщо хочаб одна міграція була застосована
            self.__set_add_tag()
            self.__set_delete_tag()
            self.__set_update_tag()
            for i in self.get_append_fields_collection():
                self.__query.insert_field_data(self.get_orm_table_name(), i)

    def extract_fields_from_db_log(self, delete=True):
        """
        Retrieves and returns all fields from the current migration table.

        Parameters
        ----------
        delete : bool
            Displays tables without the "delete" tag if the variable is False.
        Returns
        -------
        list
        """
        orm_table_name = self.get_current_migration_name()
        tables = self.__query.select_tables('*', orm_table_name, dictionary=True)
        if not delete:
            for x, i in enumerate(tables):
                if i['tag'] == bs.FIELDS_TAGS['del']:
                    del tables[x]
            return tables
        else:
            return tables

    def apply(self):
        """
        Creates tables and columns for them using migration.

        Returns
        -------
        None
        """
        last_mgr = [i for i in self.__query.show_tables() if 'mgr' in i[0]][-1][0]
        if self.__query.select_tables('*', 'current_migration'):
            current_mgr = self.__query.select_tables('current_migration', 'current_migration')[0][0]
        else:
            current_mgr = None

        # якщо остання і поточна міграції не збігаються
        if last_mgr != current_mgr:
            self.__query = Query(bs.DATABASE_USER)
            self.__query.create_db(bs.DATABASE_USER['database'])

            self.__query = Query(bs.DATABASE_ORM)
            all_tables_names_query = self.__query.custom_query('SHOW TABLES', db_connection=True)
            tables_names = [i[0] for i in all_tables_names_query if 'mgr' in i[0]]

            # якщо застосованих міграцій досі не було
            if not self.__query.select_tables('*', 'current_migration'):
                self.__query.insert_field_data('current_migration', {'current_migration': tables_names[len(tables_names)-1]})
                migration_extract = self.extract_fields_from_db_log()

                # застосування міграції
                self.__query = Query(bs.DATABASE_USER)
                self.__apply_first_migration(migration_extract)
            else:
                self.__query = Query(bs.DATABASE_ORM)
                self.__query.delete_table_data('current_migration')
                self.__query.insert_field_data('current_migration', {'current_migration': tables_names[len(tables_names)-1]})
                migration_extract = self.extract_fields_from_db_log()
                tables = self.__query.select_tables('*', 'tables', dictionary=True)

                # застосування міграції
                self.__query = Query(bs.DATABASE_USER)
                self.__apply_migration(migration_extract)
                self.__table_validation(tables)
        else:
            print('No new migrations found.')

    def _set_tables_names(self, tn):
        """

        Parameters
        ----------
        tn : str
            Table name.
        Returns
        -------
        None
        """
        self.__tables_names.add(tn)

    def _set_append_fields_collection(self, collection: dict):
        """

        Parameters
        ----------
        collection: dict
            A dictionary that describes the field.
        Returns
        -------
        None
        """
        self.__append_fields_collection.append(collection)

    def __set_add_tag(self):
        """
        Sets the field to the "add" tag.

        Returns
        -------
        None
        """
        orm_tables = self.extract_fields_from_db_log(delete=False)
        for i in self.get_append_fields_collection():
            for j in orm_tables:
                if j['tag'] == bs.FIELDS_TAGS['no']:
                    # якщо поле не знайдено в таблиці
                    if not i['field_name'] in [j['field_name'] for j in orm_tables]:
                        i['tag'] = bs.FIELDS_TAGS['add']

    def __set_add_tag_tables(self, orm_tables_names):
        """
        Sets the "add" tag to the table.

        Returns
        -------
        None
        """
        for i in self.get_append_fields_collection():
            if not i['field_name'] in orm_tables_names:
                i['tag'] = bs.FIELDS_TAGS['add']

    def __set_delete_tag_tables(self):
        """
        Sets the "delete" tag to the table.

        Returns
        -------
        None
        """
        tn = [i for i in self.__query.select_tables('*', 'tables', dictionary=True)]
        for i in tn:
            if not i['table_name'] in self.get_tables_names():
                i['tag'] = bs.FIELDS_TAGS['del']
                self.__query.update_field('tables', 'tag', bs.FIELDS_TAGS['del'], 'table_name', i['table_name'])
            else:
                self.__query.update_field('tables', 'tag', bs.FIELDS_TAGS['no'], 'table_name', i['table_name'])

    def __set_delete_tag(self):
        """
        Sets the field to the "delete" tag.

        Returns
        -------
        None
        """
        append_fields_names = [i['field_name'] for i in self.get_append_fields_collection() if not i['tag']]
        orm_tables = self.extract_fields_from_db_log(delete=False)
        orm_fields_names = [i for i in orm_tables]
        for i in orm_fields_names:
            if not i['field_name'] in append_fields_names:
                i['tag'] = bs.FIELDS_TAGS['del']
                # видалення пункту id для запобігання дублювання поля
                i.pop('id')
                self._set_append_fields_collection(i)

    def __set_update_tag(self):
        """
        Sets the field to the "update" tag.

        Returns
        -------
        None
        """
        for i in self.get_append_fields_collection():
            if not i['tag']:
                i['tag'] = bs.FIELDS_TAGS['no']
                keys = list(i.keys())
                # видалення значень які знаходяться нище для коректного порівняння полів
                # значення tag і field_table_name в однакових полях можуть бути різні після міграції
                keys.remove('tag')
                keys.remove('field_table_name')
                for j in self.extract_fields_from_db_log(delete=False):
                    if j['field_name'] == i['field_name']:
                        for key in keys:
                            if not j[key] == i[key]:
                                i['tag'] = bs.FIELDS_TAGS['upd']

    def __apply_first_migration(self, migration_extract):
        """
        Applying migration without regard tags. In this case, the method is for the first application of the
        migration.

        Parameters
        ----------
        migration_extract: list
            Data from the current migration table.
        Returns
        -------
        None
        """
        for i in migration_extract:
            self.__query.create_table(i['field_table_name'], f'CREATE TABLE {i["field_table_name"]} (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT)')
            self.__query.add_columns(i['field_table_name'], i['field_name'], i['type'], i['lenght'], i['isnull'])

    def __apply_migration(self, migration_extract):
        """
        Apply tag-aware migrations and perform appropriate actions. Creation of new tables and fields to them.
        Validation of old fields in tables.

        Parameters
        ----------
        migration_extract: list
            Data from the current migration table.
        Returns
        -------
        None
        """

        # створення нових таблиць
        tables_names = set(i['field_table_name'] for i in migration_extract)
        show_tables = [i[0] for i in self.__query.show_tables()]
        add_tables = [i for i in tables_names if not i.lower() in show_tables]
        if add_tables:
            for i in add_tables:
                self.__query.create_table(i, f'CREATE TABLE {i} (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT)')

        for i in migration_extract:
            match i['tag']:
                case 'delete':
                    self.__query.delete_column(i['field_table_name'], i['field_name'])
                case 'add':
                    self.__query.add_columns(i['field_table_name'], i['field_name'], i['type'], i['lenght'], i['isnull'])
                case 'update':
                    self.__query.update_colums(i['field_table_name'], i['field_name'], i['type'], i['lenght'], i['isnull'])

    def __table_validation(self, tables):
        """
        Table validation. Delete tables tagged "delete" from user database tables and log tables.

        Parameters
        ----------
        tables: list
            List of table fields from the ORM database.
        Returns
        -------
        None
        """

        # видалення таблиці із бази даних користувача
        for i in tables:
            if i['tag'] == bs.FIELDS_TAGS['del']:
                self.__query.delete_table(i['table_name'])

        # видалення поля бази даних із ORM таблиці
        self.__query = Query(bs.DATABASE_ORM)
        tab = self.__query.select_tables_w('*', 'tables', f"`tag` = 'delete'", dictionary=True)
        for i in tab:
            self.__query.delete_row('tables', 'table_name', i['table_name'])
        self.__query = Query(bs.DATABASE_USER)
