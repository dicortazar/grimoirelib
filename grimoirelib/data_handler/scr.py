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


import pandas

class SCR(object):
    """ Source Code Review class to deal with source code activity
       measurements.
    """

    METRICS_SUM = []

    PERIOD_WEEK = "week"
    PERIOD_MONTH = "month"
    PERIOD_YEAR = "year"

    # Constants used to check what metrics are needed to be counted and
    # what metrics are needed to be sized.
    # When aggregating values, we're interested in counting distinct 
    # companies, but when aggregating added_lines, we're interested in 
    # adding all of them.

    def __init__(self, dataset):
        """ This class expects either a database connection or a pandas dataframe

        If a pandas dataframe is not provided, then, this class needs a database
        connection.
        """

        self.data = dataset
        self.metrics = self.data.columns.values.tolist()

    def agg(self, metrics):
        """ This returns the selected metrics number for the filtered dataset
        """

        data = {}
        for metric in metrics:
            if metric in SCR.METRICS_SUM:
                data[metric] = self.data[metric].sum()
            else:
                # Counting unique values of the metric
                # eg: counting unique authors or companies
                data[metric] = self.data[metric].nunique()

        return data

    def ts(self, period):
        """ This returns the selected metrics in a timeseries format.

        This analysis is a specialization of the group method. In this
        case the selected metrics are grouped by the 'group' year, month,
        week, etc.
        """

    def group(self, groups):
        """ This group the selected 'metrics' into the specified 'groups'

        This method does not check if the group order makes sense.
        As an example, let's assume there are two metrics: commits and authors.

        Grouping commits by author makes sense, but not the other way around.
        However, if authors are grouped by commit, this method would return
        the whole list given that there would not be any actual group action.

        The order of the group is important. Data will be returned following
        that order.
        """

        data = {}

        # checking all of the groups exist
        for group in groups:
            if group not in self.metrics:
                raise Exception

        # grouping data by the selected groups in the specified order
        grouped = self.data.groupby(groups)

        aggregation = {}
        for metric in self.metrics:
            if metric not in groups:
                # if metric is in groups, it does not make sense this aggregation
                if metric in SCR.METRICS_SUM:
                    aggregation[metric] = sum
                else:
                    aggregation[metric] = pandas.Series.nunique

        return grouped.aggregate(aggregation)


