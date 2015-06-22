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

from grimoirelib.data_handler.scr import SCR

class SCRData(object):
    """ Basic class to deal with SCR data
    """

    def _connect(self):
        user = "root"
        password = ""
        host = "localhost"
        db = "wikimedia_gerrit_20150621"

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
        query = """select i.id as issue_id,
                          i.tracker_id as tracker,
                          i.type as issue_type,
                          i.status as issue_status,
                          i.resolution as issue_resolution,
                          i.priority as issue_priority,
                          i.submitted_by as submitter,
                          enr.organization_id as organization
                   from issues i
                   left join  people_uidentities pup
                        on i.submitted_by = pup.people_id
                   left join wikimedia_identities_20150621.enrollments enr
                        on pup.uuid = enr.uuid
                """

        self.data = self._execute_query(cursor, query)

    def get_data(self):
        return SCR(pandas.DataFrame(list(self.data), columns=["issue_id", "tracker", "issue_type", "issue_status", "issue_resolution", "issue_priority", "submitter", "organization"]))

