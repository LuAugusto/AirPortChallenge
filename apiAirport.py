from flask import Flask
from flask_restplus import Api, Resource
from flask import Response
from datetime import datetime
from main import server
from request import Request

app, api = server.app, server.api

def verifyIata(iataOrigem, iataVolta, dataIda, dataVolta):
    date1 = datetime.strptime(dataIda, '%Y-%m-%d').date()
    date2 = datetime.strptime(dataVolta, '%Y-%m-%d').date()

    if iataOrigem == iataVolta:
        return False
    elif date2 <= date1:
        return False

@api.route('/voo/<iataOrigem>/<iataDestino>/<dataIda>', defaults={"dataVolta":None})
@api.route('/voo/<iataOrigem>/<iataDestino>/<dataIda>/<dataVolta>')
class ApiAirport(Resource):
    def get(self, iataOrigem, iataDestino, dataIda, dataVolta):
        origem = str(iataOrigem)
        destino = str(iataDestino)
        ida = str(dataIda)
        volta = str(dataVolta) if dataVolta else None

        verifyData = verifyIata(origem, destino, ida, volta)

        if verifyData == False:
            return ({'error':'Origem e destino iguais'}, 400)

        data = Request(origem,destino, ida, volta)

        dataVoo = data.requestApi()

        if dataVoo == False:
            return ({'error': 'iata inexistente'}, 400)

        return dataVoo
