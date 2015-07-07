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

from grimoirelib_settings.settings import Settings

class SCMData(object):
    """ Basic class to deal with SCM data
    """

    def _connect(self, user, password, database):
        user = user
        password = password
        host = "localhost"
        db = database

        try:
            db = MySQLdb.connect(user = user, passwd = password, db = db, charset='utf8')
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


    def __init__(self, user, password, database, identities):
        self.identities = identities
        self.db, self.cursor = self._connect(user, password, database)
        query = """ SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = '%s' AND
                          table_name = '%s'
                """ % (database, Settings.SCM_METATABLE_NAME)

        self.columns = []
        columns_string = ""
        table_columns = self._execute_query(self.cursor, query)
        print table_columns
        for column in table_columns:
            self.columns.append(column[0])
            if len(columns_string) > 0:
                columns_string = columns_string + ","
            columns_string = columns_string + column[0]

        print columns_string
        query = "select %s from %s" % (columns_string, Settings.SCM_METATABLE_NAME)
        self.data = self._execute_query(self.cursor, query)

    def get_data(self):
        return SCM(pandas.DataFrame(list(self.data), columns=self.columns))

    def people(self):
        query = """ SELECT p.id as author,
                           p.name as name
                    FROM people p
                """
        people = self._execute_query(self.cursor, query)
        data = {}
        data["author"] = []
        data["name"] = []
        for person in people:
            data["author"].append(person[0])
            data["name"].append(person[1])
        return data

    def organizations(self):
        query = """ SELECT id as company,
                           name as name
                    FROM %s.organizations
                """ % (self.identities)
        organizations = self._execute_query(self.cursor, query)
        data = {}
        data["organization"] = []
        data["name"] = []
        for org in organizations:
            data["organization"].append(org[0])
            data["name"].append(org[1])
        return data

    def countries(self):
        query = """ SELECT code as country,
                           name as name
                    FROM %s.countries
                """ % (self.identities)
        countries = self._execute_query(self.cursor, query)
        data = {}
        data["country"] = []
        data["name"] = []
        for country in countries:
            data["country"].append(country[0])
            data["name"].append(country[1])
        return data

    def repositories(self):
        query = """ SELECT id as repository,
                           uri as uri,
                           name as name
                    FROM repositories
                """
        repositories = self._execute_query(self.cursor, query)
        data = {}
        data["repository"] = []
        data["uri"] = []
        data["name"] = []
        for repo in repositories:
            data["repository"].append(repo[0])
            data["uri"].append(repo[1])
            data["name"].append(repo[2])
        return data

