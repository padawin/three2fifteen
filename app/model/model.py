# -*- coding: utf-8 -*-

"""
This module provides the needed tools to execute the basic CRUD operations
on a database (Insert, update, delete, load all elements, load
elements from a pk, load rows from a given condition...).
"""

import psycopg2


class Model(object):
    """
    This is the base class.
    If a model class has to use it, it must extends it.
    From this point, the table associated to the class will be the module name,
    the table's primary key will be id_<module-name>
    """

    _db = None

    _table = None

    _defaultDB = None

    @classmethod
    def getClass(cls):
        return cls.__module__.split('.').pop()

    # public:
    @classmethod
    def fetchAllRows(cls, query, params={}):
        """
        c.fetchAllRows(query, params) -> list()

        Returns all the rows of the given query with the given parameters.

        @param query string Sql query to execute
        @param params dict the query's parameters

        @return list the result of the query, will be a list of dict, and
            an empty list if there's no result.
        """

        c = cls._db.cursor()
        c.execute(query, list(params))

        # Get the columns names
        column_names = [d[0] for d in c.description]
        result = c.fetchall()
        resultList = list()
        for r in result:
            resultList.append(cls._createRow(r, column_names))

        return resultList

    @classmethod
    def fetchOneRow(cls, query, params={}):
        """
        c.fetchOneRow(query, params) -> dict()

        Returns the first row of the given query with the given parameters.

        @param query string Sql query to execute
        @param params dict the query's parameters

        @return dict the result of the query, will be a dict, and
            an empty dict if there's no result.
        """

        c = cls._db.cursor()
        result = dict()
        c.execute(query, params)
        r = c.fetchone()

        # Get the columns names
        column_names = [d[0] for d in c.description]
        if r is not None:
            result = cls._createRow(r, column_names)

        return result

    @classmethod
    def insert(cls, fields):
        """
        Insert a new row in the database
        """
        c = cls._db.cursor()

        fields = cls.filterFields(fields)
        fieldsNames = list(map(lambda x: '"' + x + '"', fields.keys()))
        values = ['%s'] * len(fieldsNames)
        query = "INSERT INTO %s (%s) VALUES (%s) RETURNING id_%s" % (
            cls.getClass(),
            ','.join(fieldsNames),
            ','.join(values),
            cls.getClass()
        )

        try:
            c.execute(query, list(fields.values()))
        except psycopg2.IntegrityError:
            raise DuplicateFieldError()
        except psycopg2.DataError:
            raise InvalidDataError()
        except psycopg2.ProgrammingError:
            raise InvalidDataError()
        row_id = c.fetchone()[0]

        return row_id

    @classmethod
    def update(cls, fields, where):
        c = cls._db.cursor()

        fields = cls.filterFields(fields)
        fieldsNames = map(lambda x: '"' + x + '" = %s', fields.keys())

        query = ("UPDATE %(table)s SET %(values)s WHERE %(where)s" %
                 {
                     'table': cls.getClass(),
                     'values': ','.join(fieldsNames),
                     'where': where[0]
                 })
        c.execute(query, list(fields.values()) + where[1])

    @classmethod
    def delete(cls, where):
        c = cls._db.cursor()

        query = ("DELETE FROM %(table)s WHERE %(where)s" %
                 {'table': cls.getClass(), 'where': where[0]})
        c.execute(query, where[1])

    @classmethod
    def connect(cls, conn_string):
        try:
            cls._db = psycopg2.connect(conn_string)
        except psycopg2.OperationalError:
            raise ConnectionError("Failed to connect to database");

    @classmethod
    def disconnect(cls):
        if cls._db is not None:
            cls._db.close()

    @classmethod
    def begin(cls):
        cls._db.begin()

    @classmethod
    def commit(cls):
        cls._db.commit()

    @classmethod
    def rollback(cls):
        cls._db.rollback()

    @staticmethod
    def _createRow(sqliteRow, columns):
        row = {}
        for i, v in enumerate(sqliteRow):
            row[columns[i]] = v

        return row

    @classmethod
    def loadAll(cls, fields=None, order_fields={}):
        fields = cls.prepareFieldsForSelect(fields)
        order = ''
        if len(order_fields):
            order = 'ORDER BY {}'.format(
                ', '.join("{} {}".format(field, way)
                          for field, way in order_fields.items())
            )

        query = """
            SELECT
                %(fields)s
            FROM
                %(table)s
            %(order)s
        """ % {'fields': fields, 'table': cls.getClass(), 'order': order}

        return cls.fetchAllRows(query)

    @classmethod
    def loadById(cls, id, fields=None):
        fields = cls.prepareFieldsForSelect(fields)

        table = cls.getClass()
        query = """
            SELECT
                %(fields)s
            FROM
                %(table)s
            WHERE
                %(where)s
        """ % {
            'fields': fields,
            'table': table,
            'where': 'id_' + table + ' = %s'
        }

        try:
            return cls.fetchOneRow(query, [id])
        except psycopg2.DataError:
            return None

    @classmethod
    def loadBy(cls, filters, fields=None, order_fields={}):
        fields = cls.prepareFieldsForSelect(fields)

        filters = cls.filterFields(filters)
        filtersNames = map(lambda x: '"' + x + '" = %s', filters.keys())
        order = ''
        if len(order_fields):
            order = 'ORDER BY {}'.format(
                ', '.join("{} {}".format(field, way)
                          for field, way in order_fields.items())
            )

        query = """
            SELECT
                %(fields)s
            FROM
                %(table)s
            WHERE
                %(where)s
            %(order)s
        """ % {
            'fields': fields,
            'table': cls.getClass(),
            'where': ' AND '.join(filtersNames),
            'order': order
        }

        return cls.fetchAllRows(query, filters.values())

    @classmethod
    def prepareFieldsForSelect(cls, fields=None):
        if not fields:
            fields = cls.fields

        if isinstance(fields, list) or isinstance(fields, tuple):
            fields = ', '.join(fields)
        elif isinstance(fields, dict):
            fields = ', '.join(map(lambda x: fields[x] + ' AS ' + x, fields))
        elif not isinstance(fields, str):
            raise TypeError('Unexpected type of fields (%s)' % type(fields))

        return fields

    @classmethod
    def filterFields(cls, fields):
        return dict((k, fields[k]) for k in cls.fields if k in fields)

    @classmethod
    def executeQuery(cls, cursor, query, params):
        cursor.execute(query, params)


class DuplicateFieldError(BaseException):
    pass


class ConnectionError(BaseException):
    pass


class InvalidDataError(BaseException):
    pass
