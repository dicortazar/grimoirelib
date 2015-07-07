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


from flask import Flask, jsonify
from flask_restful import Resource, Api

from grimoirelib.db.scm_data import SCMData
from grimoirelib.db.scr_data import SCRData

app = Flask(__name__)
api = Api(app)


scm_object = SCMData("root", "", "wikimedia_git_20150629", "wikimedia_identities_20150621")
scm_data = scm_object.get_data()

#scr_object = SCRData()
#scr_data = scr_object.get_data()

## SCM metrics
class SCMMetrics(Resource):
    def get(self):
        return jsonify(metrics=scm_data.metrics)

class SCMRaw(Resource):
    def get(self):
        return jsonify(raw=scm_data.raw())

class SCMAgg(Resource):
    def get(self):
        return jsonify(agg=scm_data.agg(scm_data.metrics))

class SCMTS(Resource):
    def get(self):
        return jsonify(ts=scm_data.ts(scm_data.PERIOD_MONTH, scm_data.metrics))

## SCM List of elements

class SCMPeople(Resource):
    def get(self):
        return scm_object.people()

class SCMOrganizations(Resource):
    def get(self):
        return scm_object.organizations()

class SCMRepositories(Resource):
    def get(self):
        return scm_object.repositories()

class SCMCountries(Resource):
    def get(self):
        return scm_object.countries()


## SCR metrics
class SCRMetrics(Resource):
    def get(self):
        return jsonify(metrics=scr_data.metrics)

class SCRRaw(Resource):
    def get(self):
        return jsonify(raw=scr_data.data)

class SCRAgg(Resource):
    def get(self):
        return jsonify(agg=scr_data.agg(scr_data.metrics))


api.add_resource(SCMMetrics, "/scm/metrics/")
api.add_resource(SCMRaw, "/scm/raw/")
api.add_resource(SCMAgg, "/scm/agg/")
api.add_resource(SCMTS, "/scm/ts/")
api.add_resource(SCMPeople, "/scm/people/")
api.add_resource(SCMOrganizations, "/scm/organizations/")
api.add_resource(SCMRepositories, "/scm/repositories/")
api.add_resource(SCMCountries, "/scm/countries/")


api.add_resource(SCRMetrics, "/metrics/scr/")
api.add_resource(SCRRaw, "/raw/scr/")
api.add_resource(SCRAgg, "/agg/scr/")

if __name__ == '__main__':
    app.run(debug=True)

