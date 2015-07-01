## Copyright (C) 2014 Bitergia
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details. 
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##
## Authors:
##   Daniel Izquierdo-Cortazar <dizquierdo@bitergia.com>
##


import MySQLdb
import pandas

from grimoirelib.data_handler.scm import SCM

class SCMData(object):
    """ Basic class to deal with SCM data
    """

    def _connect(self, user, password, database):
        user = user
        password = password
        host = "localhost"
        db = database

        try:
            db = MySQLdb.connect(user = user, passwd = password, db = db)
            return db, db.cursor()
        except:
            logging.error("Database connection error")
            raise

    def _execute_query(self, connector, query):
        results = int (connector.execute(query))
        cont = 0
        if results > 0:
            result1 = connector.fetchall()
            return result1
        else:
            return []


    def __init__(self, user, password, database):
        db, cursor = self._connect(user, password, database)
        query = """ SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = '%s' AND
                          table_name = 'scm_metadata'
                """ % (database)

        self.columns = []
        columns_string = ""
        table_columns = self._execute_query(cursor, query)
        print table_columns
        for column in table_columns:
            self.columns.append(column[0])
            if len(columns_string) > 0:
                columns_string = columns_string + ","
            columns_string = columns_string + column[0]

        print columns_string
        query = "select %s from scm_metadata" % (columns_string)
        self.data = self._execute_query(cursor, query)

    def get_data(self):
        return SCM(pandas.DataFrame(list(self.data), columns=self.columns))

