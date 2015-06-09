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

from scm_data import SCMData

app = Flask(__name__)
api = Api(app)

scm_object = SCMData()
scm_data = scm_object.get_data()

class Metrics(Resource):
    def get(self):
        return jsonify(metrics=scm_data.metrics)

class Raw(Resource):
    def get(self):
        return jsonify(raw=scm_data.data)

class Agg(Resource):
    def get(self):
        return jsonify(agg=scm_data.agg(scm_data.metrics))


api.add_resource(Metrics, "/metrics")
api.add_resource(Raw, "/raw")
api.add_resource(Agg, "/agg")

if __name__ == '__main__':
    app.run(debug=True)

