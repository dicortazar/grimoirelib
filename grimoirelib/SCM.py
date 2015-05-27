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

class SCM(object):
   """ Source Code Management class to deal with source code activity
       measurements.
   """

PERIOD_WEEK = "week"
PERIOD_MONTH = "month"
PERIOD_YEAR = "year"


    def __init__(self):
        """ This class expects either a database connection or a pandas dataframe

        If a pandas dataframe is not provided, then, this class needs a database
        connection.
        """

    def agg(self, metrics):
        """ This returns the selected metrics number for the filtered dataset
        """

    def ts(self, metrics, period):
        """ This returns the selected metrics in a timeseries format.

        This analysis is a specialization of the group method. In this
        case the selected metrics are grouped by the 'group' year, month,
        week, etc.
        """

    def group(self, metrics, groups):
        """ This group the selected 'metrics' into the specified 'groups'

        This method does not check if the group order makes sense.
        As an example, let's assume there are two metrics: commits and authors.

        Grouping commits by author makes sense, but not the other way around.
        However, if authors are grouped by commit, this method would return
        the whole list given that there would not be any actual group action.
        """

    def metrics(self):
        """ This returns a list with available metrics
        """

