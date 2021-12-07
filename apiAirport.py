from flask import Flask
from flask_restplus import Api, Resource

from main import server

app, api = server.app, server.api

data = [
    {'id':0, 'title':'War and Peace'}
]

@api.route('/air')
class ApiAirport(Resource):
    def get(self):
        return data