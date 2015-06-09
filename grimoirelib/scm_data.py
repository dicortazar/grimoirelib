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

from scm import SCM

class SCMData(object):
    """ Basic class to deal with SCM data
    """

    def _connect(self):
        user = "root"
        password = ""
        host = "localhost"
        db = "eclipse_source_code_20141127"

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


    def __init__(self):
        db, cursor = self._connect()
        query = """select cl.added,
                       cl.removed,
                       s.author_date,
                       s.author_id,
                       s.repository_id,
                       upc.company_id
                   from commits_lines cl,
                        scmlog s,
                        people_upeople pup,
                        upeople_companies upc
                   where cl.commit_id = s.id and
                        s.author_id=pup.people_id and
                        pup.upeople_id = upc.upeople_id limit 10"""

        self.data = self._execute_query(cursor, query)
        print self.data

    def get_data(self):
        print self.data
        return SCM(pandas.DataFrame(list(self.data), columns=["added_lines", "removed_lines", "date", "author", "repository", "company"]))

